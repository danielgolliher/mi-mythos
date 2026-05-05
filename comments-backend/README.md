# MI Mythos Comments Backend

A tiny Cloudflare Worker that gives the example briefs **shared, cross-device comments** with **IP-segregated commenter IDs** ("Commenter 1, 2, 3…" assigned per page based on the first commenting IP).

Without this Worker, comments still work — they're just **device-local**: every visitor sees only the comments they themselves posted in their own browser.

## Deploy in ~5 minutes

```bash
# 1. Install Wrangler if you don't have it
npm install -g wrangler

# 2. Authenticate to Cloudflare (free account is fine)
wrangler login

# 3. From this directory:
cd comments-backend

# 4. Create a KV namespace for storage
wrangler kv:namespace create COMMENTS
# → copy the printed `id = "..."` into wrangler.toml

# 5. (Optional) Set a private salt for IP hashing
wrangler secret put IP_SALT
# → paste any random string when prompted

# 6. Deploy
wrangler deploy
# → prints the deployed URL, e.g. https://mi-mythos-comments.<your-subdomain>.workers.dev
```

## Wire the briefs to the Worker

In each example brief (`examples/electronic-rent-payments/index.html` and
`examples/teacher-cba-student-outcomes/index.html`), find the line near the
top of the comments script:

```js
const COMMENTS_ENDPOINT = null;
```

Change it to your deployed Worker URL plus `/api/comments`:

```js
const COMMENTS_ENDPOINT = 'https://mi-mythos-comments.your-subdomain.workers.dev/api/comments';
```

Commit and push. From that moment on, every visitor's comments are stored in
the Worker's KV namespace and visible to everyone else.

## How user identification works

- The Worker reads the visitor's IP from Cloudflare's `CF-Connecting-IP`
  header (this only works because Cloudflare proxies the request).
- The IP is **hashed with SHA-256 and a private salt before storage**. Raw
  IPs are never written to KV.
- The first hashed IP to post on a given page is assigned `Commenter 1`,
  the second new IP becomes `Commenter 2`, etc. The mapping is stored under
  `users:<page>:<ipHash>` and is **per-page** — the same person commenting
  on two different briefs gets two different sequential numbers.
- Color is derived deterministically from the IP hash, so the same person
  always shows up in the same color across visits.

## Endpoints

```
GET  /api/comments?path=/examples/teacher-cba-student-outcomes
  → 200 OK, JSON array of comments

POST /api/comments
  Content-Type: application/json
  Body: { path: "/examples/...", comment: { anchor, body, ... } }
  → 200 OK, { ok: true, comment: <stored> }

DELETE /api/comments?path=/examples/...&id=<comment-id>
  → 200 OK, { ok: true }
  → 403 if the requesting IP didn't post this comment
  → 404 if no comment with that id exists
```

The server **overrides** any client-claimed `author` field with the IP-derived
identity on POST, so a visitor cannot impersonate another commenter.

DELETE is **author-only**: the server verifies that the requesting IP's hash
matches the comment's stored `author.id`. A visitor cannot delete someone
else's comments. (The frontend hides the delete button for non-author
comments, but the server enforces this independently.)

## Limits

- Per-page cap: 500 comments. Adjust in `worker.js` if you want more.
- Comment body cap: 5,000 characters.
- Anchor text: 1,000 characters max for the highlighted text.
- Cloudflare free tier: 100,000 Worker requests/day, 100,000 KV reads/day,
  1,000 KV writes/day. More than enough for any reasonable use of this site.

## Privacy notes

- IP addresses are never stored — only their salted SHA-256 hashes (16
  characters of base64), which are not reversible to the source IP without
  brute-forcing the entire IPv4 space against the salt.
- No cookies, no tracking, no analytics. The Worker only stores what's needed
  to render the comments themselves.
- If you set `IP_SALT` to a private string (recommended), even someone with
  full read access to your KV cannot reverse the hashes back to IPs without
  also having the salt.
