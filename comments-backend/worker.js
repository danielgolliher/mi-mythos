/**
 * MI Mythos comments backend — Cloudflare Worker.
 *
 * Deploy this Worker to enable shared, IP-segregated comments across all visitors
 * to the example briefs. Without it, comments are stored device-locally in
 * each visitor's localStorage (the default).
 *
 * Storage: a single Cloudflare KV namespace.
 *   - "comments:<page>"  →  JSON array of comments
 *   - "users:<ipHash>"   →  { id, label, color, bgColor, count }   (sequential per page)
 *   - "counter:<page>"   →  number  (used to assign Commenter 1, 2, 3...)
 *
 * Endpoints:
 *   GET    /api/comments?path=<pagepath>             → 200 JSON array
 *   POST   /api/comments                             → body { path, comment } → 200 { ok: true }
 *   DELETE /api/comments?path=<pagepath>&id=<cid>    → 200 { ok: true }
 *                                                      403 if requesting IP didn't post the comment
 *   POST   /api/user                                 → body { path, name } → 200 { ok: true, user }
 *                                                      Sets the user's custom display name and
 *                                                      rewrites author labels on all of their
 *                                                      existing comments on this page.
 *
 * The Worker reads CF-Connecting-IP (set by Cloudflare's edge), hashes it with
 * SHA-256, and uses the hash as the per-user key. Raw IPs are never stored.
 *
 * To deploy:
 *   1. npm install -g wrangler
 *   2. wrangler login
 *   3. wrangler kv:namespace create COMMENTS
 *   4. Copy the namespace ID into wrangler.toml (alongside this file)
 *   5. wrangler deploy
 *   6. Copy the deployed URL into the brief's COMMENTS_ENDPOINT constant
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

// Derive a stable, opaque user ID from an IP address. SHA-256 hash, base64-encoded.
async function hashIP(ip, salt) {
  const data = new TextEncoder().encode(ip + ':' + (salt || ''));
  const buf = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(buf))).slice(0, 16);
}

// Deterministic color from a user hash.
function colorFromHash(hash) {
  let h = 0;
  for (let i = 0; i < hash.length; i++) h = (h * 31 + hash.charCodeAt(i)) % 360;
  return {
    color: `hsl(${h}, 65%, 45%)`,
    bgColor: `hsla(${h}, 70%, 55%, 0.28)`,
  };
}

// Get-or-create a per-page user record. The first IP to comment on a page is
// "Commenter 1" on that page; the second new IP is "Commenter 2"; and so on.
// `defaultLabel` is the assigned sequential label; `name` is an optional custom
// override; `label` is what's displayed (= name || defaultLabel).
async function getOrCreateUser(env, page, ipHash) {
  const userKey = `users:${page}:${ipHash}`;
  const existing = await env.COMMENTS.get(userKey, 'json');
  if (existing) {
    if (!existing.defaultLabel) existing.defaultLabel = existing.label || `Commenter ?`;
    if (existing.name === undefined) existing.name = null;
    existing.label = existing.name || existing.defaultLabel;
    return existing;
  }
  const counterKey = `counter:${page}`;
  const cur = parseInt((await env.COMMENTS.get(counterKey)) || '0', 10);
  const next = cur + 1;
  const { color, bgColor } = colorFromHash(ipHash);
  const defaultLabel = `Commenter ${next}`;
  const user = {
    id: ipHash,
    defaultLabel,
    name: null,
    label: defaultLabel,
    color,
    bgColor,
  };
  await env.COMMENTS.put(userKey, JSON.stringify(user));
  await env.COMMENTS.put(counterKey, String(next));
  return user;
}

function jsonResponse(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS, ...extraHeaders },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const ipHash = await hashIP(ip, env.IP_SALT || 'mi-mythos-default-salt');

    if (url.pathname === '/api/user') {
      if (request.method === 'POST') {
        let body;
        try { body = await request.json(); }
        catch { return jsonResponse({ error: 'invalid JSON' }, 400); }
        const page = body.path;
        if (!page) return jsonResponse({ error: 'missing path' }, 400);

        // Load (or create) the user record
        const user = await getOrCreateUser(env, page, ipHash);
        const newName = body.name == null ? null : String(body.name).slice(0, 40).trim() || null;
        user.name = newName;
        user.label = user.name || user.defaultLabel;
        await env.COMMENTS.put(`users:${page}:${ipHash}`, JSON.stringify(user));

        // Rewrite author labels on this user's existing comments on this page
        const comments = (await env.COMMENTS.get(`comments:${page}`, 'json')) || [];
        let changed = false;
        for (const c of comments) {
          if (c.author && c.author.id === ipHash) {
            c.author.name = user.name;
            c.author.label = user.label;
            changed = true;
          }
        }
        if (changed) await env.COMMENTS.put(`comments:${page}`, JSON.stringify(comments));

        return jsonResponse({ ok: true, user });
      }
      return jsonResponse({ error: 'method not allowed' }, 405);
    }

    // Admin-only: set a lifecycle status on a comment ("deployed", "rolled back",
    // or null to clear). Requires the ADMIN_TOKEN secret.
    if (url.pathname === '/api/status') {
      if (request.method !== 'POST') return jsonResponse({ error: 'method not allowed' }, 405);
      let body;
      try { body = await request.json(); }
      catch { return jsonResponse({ error: 'invalid JSON' }, 400); }
      if (!env.ADMIN_TOKEN || body.token !== env.ADMIN_TOKEN) {
        return jsonResponse({ error: 'forbidden' }, 403);
      }
      const ALLOWED = ['deployed', 'rolled back', 'rollback requested', null];
      if (!ALLOWED.includes(body.status)) return jsonResponse({ error: 'bad status' }, 400);
      if (!body.path || !body.id) return jsonResponse({ error: 'missing path/id' }, 400);
      const list = (await env.COMMENTS.get(`comments:${body.path}`, 'json')) || [];
      const target = list.find((c) => c.id === body.id);
      if (!target) return jsonResponse({ error: 'comment not found' }, 404);
      target.status = body.status;
      await env.COMMENTS.put(`comments:${body.path}`, JSON.stringify(list));
      return jsonResponse({ ok: true, comment: target });
    }

    // Public: request rollback of a deployed feature. Only transitions
    // "deployed" -> "rollback requested"; every other state is rejected.
    if (url.pathname === '/api/rollback-request') {
      if (request.method !== 'POST') return jsonResponse({ error: 'method not allowed' }, 405);
      let body;
      try { body = await request.json(); }
      catch { return jsonResponse({ error: 'invalid JSON' }, 400); }
      if (!body.path || !body.id) return jsonResponse({ error: 'missing path/id' }, 400);
      const list = (await env.COMMENTS.get(`comments:${body.path}`, 'json')) || [];
      const target = list.find((c) => c.id === body.id);
      if (!target) return jsonResponse({ error: 'comment not found' }, 404);
      if (target.status !== 'deployed') {
        return jsonResponse({ error: 'only deployed features can be rolled back' }, 409);
      }
      target.status = 'rollback requested';
      await env.COMMENTS.put(`comments:${body.path}`, JSON.stringify(list));
      return jsonResponse({ ok: true, comment: target });
    }

    if (url.pathname === '/api/comments') {
      // GET/DELETE take ?path=...; POST carries path in the JSON body
      // (per the documented API), with the query param as a fallback.
      let page = url.searchParams.get('path') || '';

      if (request.method === 'GET') {
        if (!page) return jsonResponse({ error: 'missing path' }, 400);
        const list = (await env.COMMENTS.get(`comments:${page}`, 'json')) || [];
        return jsonResponse(list);
      }

      if (request.method === 'POST') {
        let body;
        try { body = await request.json(); }
        catch { return jsonResponse({ error: 'invalid JSON' }, 400); }
        page = page || String(body.path || '');
        if (!page) return jsonResponse({ error: 'missing path' }, 400);
        if (!body.comment || !body.comment.body || !body.comment.anchor) {
          return jsonResponse({ error: 'invalid comment shape' }, 400);
        }
        // Server overrides client-claimed identity with IP-derived identity
        const user = await getOrCreateUser(env, page, ipHash);
        const sanitized = {
          id: body.comment.id || crypto.randomUUID(),
          anchor: {
            sectionId: String(body.comment.anchor.sectionId || ''),
            prefix: String(body.comment.anchor.prefix || '').slice(0, 200),
            exact: String(body.comment.anchor.exact || '').slice(0, 1000),
            suffix: String(body.comment.anchor.suffix || '').slice(0, 200),
          },
          body: String(body.comment.body || '').slice(0, 5000),
          author: user,
          createdAt: Date.now(),
        };
        const list = (await env.COMMENTS.get(`comments:${page}`, 'json')) || [];
        // Cap per-page to 500 comments to bound storage cost
        if (list.length >= 500) return jsonResponse({ error: 'comment cap reached' }, 429);
        list.push(sanitized);
        await env.COMMENTS.put(`comments:${page}`, JSON.stringify(list));
        return jsonResponse({ ok: true, comment: sanitized });
      }

      if (request.method === 'DELETE') {
        if (!page) return jsonResponse({ error: 'missing path' }, 400);
        const id = url.searchParams.get('id');
        if (!id) return jsonResponse({ error: 'missing id' }, 400);
        const list = (await env.COMMENTS.get(`comments:${page}`, 'json')) || [];
        const target = list.find((c) => c.id === id);
        if (!target) return jsonResponse({ error: 'comment not found' }, 404);
        // Authorize: requesting IP hash must match the comment's author.id
        if (target.author && target.author.id !== ipHash) {
          return jsonResponse({ error: 'forbidden — not the author' }, 403);
        }
        const filtered = list.filter((c) => c.id !== id);
        await env.COMMENTS.put(`comments:${page}`, JSON.stringify(filtered));
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: 'method not allowed' }, 405);
    }

    return jsonResponse({ error: 'not found' }, 404);
  },
};
