#!/usr/bin/env python3
"""Inject the MI Mythos password gate into a brief. Idempotent.

The gate is a soft barrier — anyone who can read source can bypass it.
The password is stored as a SHA-256 hash to avoid having the literal string
embedded. The check is case-insensitive (input upper-cased before hashing).

To rotate the password:
  1. Compute new hash:  printf '%s' 'NEWPASSWORD' | shasum -a 256
  2. Replace PASSWORD_HASH below
  3. Re-run this script over every brief
"""
import sys

# SHA-256 of "MIMYTHOS"
PASSWORD_HASH = '0e3531e9f9fed4f1aa180fde6a148a8fd8ac006a733b06e806f56e87d60cb84e'
STORAGE_KEY = 'mi-mythos-unlocked'

# 1. Inline head script that runs synchronously BEFORE body renders.
#    If unlocked, adds class="unlocked" to <html> so the gate CSS hides itself
#    immediately — no flash for returning visitors.
HEAD_SCRIPT = f"""<script>
(function() {{
  try {{
    if (localStorage.getItem('{STORAGE_KEY}') === 'true') {{
      document.documentElement.classList.add('unlocked');
    }}
  }} catch (e) {{}}
}})();
</script>
"""

# 2. CSS — the gate fills the viewport with the same parchment palette and
#    sits above all other content via z-index.
CSS = """  /* === PASSWORD GATE === */
  .password-gate {
    position: fixed;
    inset: 0;
    background: var(--bg);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  html.unlocked .password-gate { display: none; }
  html:not(.unlocked) body { overflow: hidden; }
  .gate-card {
    max-width: 440px;
    width: 100%;
    background: #fff;
    border: 1px solid var(--rule);
    border-radius: 6px;
    padding: 36px 32px 32px;
    text-align: center;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    font-family: "Iowan Old Style", "Charter", Georgia, serif;
  }
  .gate-card .gate-kicker {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--muted);
    margin: 0 0 12px;
    font-weight: 600;
  }
  .gate-card .gate-title {
    font-size: 32px;
    margin: 0 0 12px;
    font-weight: 700;
    line-height: 1.1;
  }
  .gate-card .gate-deck {
    font-size: 16px;
    color: var(--muted);
    font-style: italic;
    margin: 0 0 24px;
  }
  #gate-input {
    width: 100%;
    border: 1px solid var(--rule);
    border-radius: 3px;
    padding: 12px 14px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 16px;
    letter-spacing: 0.05em;
    text-align: center;
    background: var(--bg);
    color: var(--ink);
    margin-bottom: 12px;
    box-sizing: border-box;
  }
  #gate-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(107, 52, 16, 0.12);
  }
  .gate-submit {
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 11px 24px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    cursor: pointer;
    border-radius: 3px;
    width: 100%;
  }
  .gate-submit:hover { background: #8c4f25; }
  .gate-error {
    color: #b41e1e;
    font-size: 13px;
    margin: 14px 0 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  .gate-error[hidden] { display: none; }
  .password-gate.shake .gate-card { animation: gate-shake 0.4s; }
  @keyframes gate-shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    75% { transform: translateX(8px); }
  }
  @media (max-width: 540px) {
    .gate-card { padding: 28px 22px 24px; }
    .gate-card .gate-title { font-size: 26px; }
    .gate-card .gate-deck { font-size: 15px; }
  }
  @media print {
    .password-gate { display: none !important; }
  }
"""

# 3. HTML — placed as the FIRST child of <body> so it renders before any other
#    content paints.
HTML = """<div class="password-gate" id="password-gate" role="dialog" aria-labelledby="gate-title">
  <form class="gate-card" id="gate-form" autocomplete="off">
    <p class="gate-kicker">MI Mythos</p>
    <h1 class="gate-title" id="gate-title">Restricted</h1>
    <p class="gate-deck">Enter the access password to view this brief. You'll only need to do this once.</p>
    <input type="password" id="gate-input" placeholder="Password" autocomplete="off" autocapitalize="characters" spellcheck="false" required>
    <button type="submit" class="gate-submit">Unlock</button>
    <p class="gate-error" id="gate-error" hidden>That's not the right password.</p>
  </form>
</div>
"""

# 4. JS that runs AFTER body — the gate IIFE wires up the form submit.
JS = f"""<script>
(function() {{
  const STORAGE_KEY = '{STORAGE_KEY}';
  const PASSWORD_HASH = '{PASSWORD_HASH}';
  const gate = document.getElementById('password-gate');
  const form = document.getElementById('gate-form');
  const input = document.getElementById('gate-input');
  const errorEl = document.getElementById('gate-error');
  if (!gate || !form || !input) return;

  // If localStorage already says unlocked, the head script set html.unlocked,
  // which CSS uses to hide the gate. Nothing else to do here in that case.
  if (document.documentElement.classList.contains('unlocked')) return;

  setTimeout(function() {{ input.focus(); }}, 30);

  async function sha256(str) {{
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map(function(b) {{ return b.toString(16).padStart(2, '0'); }}).join('');
  }}

  form.addEventListener('submit', async function(e) {{
    e.preventDefault();
    const guess = (input.value || '').trim().toUpperCase();
    if (!guess) return;
    const hash = await sha256(guess);
    if (hash === PASSWORD_HASH) {{
      try {{ localStorage.setItem(STORAGE_KEY, 'true'); }} catch (e) {{}}
      document.documentElement.classList.add('unlocked');
      errorEl.hidden = true;
    }} else {{
      errorEl.hidden = false;
      gate.classList.add('shake');
      setTimeout(function() {{ gate.classList.remove('shake'); }}, 400);
      input.select();
    }}
  }});
}})();
</script>
"""

CSS_MARKER = '  /* === BRIEF NAVIGATION STRIP === */'
HEAD_MARKER = '<title>'  # head script goes right before <title> (or anywhere safe in head)
HTML_MARKER = '<body>'   # gate is FIRST element after <body>


def inject(path):
    with open(path) as f:
        html = f.read()
    sentinel = '/* === PASSWORD GATE === */'

    if sentinel in html:
        print('  · password gate already injected, skipping')
        return

    # 1. Head script before <title>
    if HEAD_MARKER in html:
        html = html.replace(HEAD_MARKER, HEAD_SCRIPT + HEAD_MARKER, 1)
        print('  + Head unlock-check script')
    else:
        print('  ! <title> marker not found in head')

    # 2. CSS before brief-navigation block (or before </style> as fallback)
    if CSS_MARKER in html:
        html = html.replace(CSS_MARKER, CSS + CSS_MARKER, 1)
        print('  + CSS injected')
    else:
        # fallback: before </style>
        idx = html.find('</style>')
        if idx == -1:
            raise SystemExit('No </style> found')
        html = html[:idx] + CSS + html[idx:]
        print('  + CSS injected (fallback before </style>)')

    # 3. Gate HTML as FIRST child of <body>
    if HTML_MARKER in html:
        # Insert right after <body>... line
        body_open = html.find(HTML_MARKER)
        # Find end of the body tag itself (handle <body class="..."> too)
        gt = html.find('>', body_open)
        if gt == -1:
            raise SystemExit('Malformed <body> tag')
        before = html[: gt + 1]
        after = html[gt + 1 :]
        html = before + '\n' + HTML + after
        print('  + Gate HTML inserted at top of body')
    else:
        print('  ! <body> not found')

    # 4. JS at end of body, just before </body>
    body_close = html.rfind('</body>')
    if body_close != -1:
        html = html[:body_close] + JS + '\n' + html[body_close:]
        print('  + Gate JS appended before </body>')
    else:
        print('  ! </body> not found')

    with open(path, 'w') as f:
        f.write(html)
    print(f'OK: {path}')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'\nProcessing {p}')
        inject(p)
