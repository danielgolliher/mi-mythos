#!/usr/bin/env python3
"""Inject mobile-friendliness fixes into a brief. Idempotent: safe to re-run."""
import re, sys

MOBILE_CSS = r"""  /* === MOBILE FRIENDLINESS === */
  /* Lock horizontal overflow at the root */
  html, body { max-width: 100%; overflow-x: hidden; }
  /* Long URLs in citations / sources / footnotes wrap on any boundary */
  .sources a, .citations a, .footnotes a, code {
    word-break: break-word;
    overflow-wrap: anywhere;
  }
  /* Long content that would overflow gets a horizontal scroll inside its container */
  .stat-grid, .exchange, blockquote, .pull { max-width: 100%; }
  /* Mobile TOC drawer trigger (left side; comments FAB stays on right) */
  #toc-mobile-btn {
    display: none;
    position: fixed;
    bottom: 20px; left: 20px;
    background: var(--accent); color: #fff;
    border: none; border-radius: 22px;
    height: 44px; padding: 0 14px;
    cursor: pointer;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 13px; font-weight: 600;
    box-shadow: 0 3px 10px rgba(0,0,0,0.18);
    z-index: 60;
    align-items: center; gap: 6px;
  }
  nav.toc .toc-close {
    display: none;
    position: absolute;
    top: 8px; right: 10px;
    background: transparent; border: none;
    font-size: 22px; color: var(--muted);
    cursor: pointer;
    padding: 4px 8px;
    line-height: 1;
  }
  /* Below 1180px: TOC becomes a left-edge slide-in drawer with a backdrop */
  @media (max-width: 1180px) {
    #toc-mobile-btn { display: inline-flex; }
    nav.toc {
      display: block !important;
      position: fixed;
      top: 0; left: 0; bottom: 0;
      width: min(290px, calc(100vw - 80px));
      max-height: 100vh;
      height: 100vh;
      border: none;
      border-right: 1px solid var(--rule);
      border-radius: 0;
      background: rgba(251, 250, 246, 0.98);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transform: translateX(-100%);
      transition: transform 0.22s ease-out;
      z-index: 70;
      overflow-y: auto;
      padding: 22px 20px 80px;
      box-shadow: 4px 0 14px rgba(0,0,0,0.08);
    }
    nav.toc.open { transform: translateX(0); }
    nav.toc .toc-close { display: block; }
    body.toc-open::before {
      content: "";
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.35);
      z-index: 65;
    }
  }
  /* Tighten typography and switch tables / stat-grid to mobile shapes */
  @media (max-width: 600px) {
    body { font-size: 16px; }
    .wrap { padding: 36px 18px 80px; }
    h1 { font-size: 26px; line-height: 1.18; }
    h2 { font-size: 19px; }
    h3 { font-size: 15px; }
    .deck { font-size: 16px; }
    .meta { font-size: 12px; }
    blockquote { padding: 12px 14px; font-size: 15px; }
    .pull { font-size: 18px; padding: 14px 6px; }
    .exchange { padding: 14px 16px; font-size: 15px; }
    .stat-grid { grid-template-columns: 1fr; gap: 10px; }
    .stat .num { font-size: 22px; }
    table.timeline {
      display: block;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      font-size: 13px;
    }
    table.timeline td.date { width: auto; min-width: 90px; padding-right: 4px; }
    .citations, .sources, .footnotes { padding-left: 8px; padding-right: 8px; }
    .citations ol, .footnotes ol { padding-left: 22px; }
  }
  @media (max-width: 540px) {
    #toc-mobile-btn { left: 16px; bottom: 16px; }
    sup.factref a.fact .tip,
    a.person .tip {
      width: min(260px, calc(100vw - 32px));
      max-width: calc(100vw - 32px);
    }
    h1 { font-size: 23px; }
    .pull { font-size: 17px; }
    /* Comment modal must not overflow on phones */
    .comment-modal-card { padding: 18px 18px; }
    .comment-modal-card textarea { min-height: 80px; }
  }
  @media print {
    #toc-mobile-btn { display: none !important; }
    nav.toc .toc-close { display: none !important; }
    body.toc-open::before { display: none !important; }
  }
"""

MOBILE_BUTTON = '<button id="toc-mobile-btn" type="button" aria-label="Open table of contents">📑 Contents</button>\n\n'

CLOSE_BTN_HTML = '\n  <button class="toc-close" type="button" aria-label="Close table of contents">×</button>'

MOBILE_JS_FN = """  function setupMobileTOC() {
    const btn = document.getElementById('toc-mobile-btn');
    const toc = document.querySelector('nav.toc');
    const closeBtn = toc ? toc.querySelector('.toc-close') : null;
    if (!btn || !toc) return;
    function open() {
      toc.classList.add('open');
      document.body.classList.add('toc-open');
    }
    function close() {
      toc.classList.remove('open');
      document.body.classList.remove('toc-open');
    }
    btn.addEventListener('click', function(e) { e.stopPropagation(); open(); });
    if (closeBtn) closeBtn.addEventListener('click', close);
    toc.addEventListener('click', function(e) {
      if (e.target.tagName === 'A') close();
    });
    document.addEventListener('click', function(e) {
      if (!document.body.classList.contains('toc-open')) return;
      if (e.target.closest('nav.toc, #toc-mobile-btn')) return;
      close();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && document.body.classList.contains('toc-open')) close();
    });
  }

"""

def inject(path):
    with open(path) as f:
        html = f.read()

    # 1. Add the mobile CSS right before "</style>" (the FIRST one in the file is the head's)
    # Re-running is safe because we check for a sentinel marker.
    if '/* === MOBILE FRIENDLINESS === */' not in html:
        # Insert at the last </style> before </head>
        marker_idx = html.find('</style>')
        if marker_idx == -1:
            raise SystemExit('No </style> tag found')
        html = html[:marker_idx] + MOBILE_CSS + html[marker_idx:]
        print('  + Added mobile CSS')

    # 2. Add the TOC close button INSIDE nav.toc, after the toc-label paragraph.
    if '<button class="toc-close"' not in html:
        # Inject right after the opening <nav class="toc"...>
        m = re.search(r'(<nav class="toc"[^>]*>)', html)
        if m:
            insert_at = m.end()
            html = html[:insert_at] + CLOSE_BTN_HTML + html[insert_at:]
            print('  + Added TOC close button')

    # 3. Add the mobile-TOC trigger button right before <button id="comments-fab">
    if 'id="toc-mobile-btn"' not in html:
        marker = '<button id="comments-fab"'
        if marker in html:
            html = html.replace(marker, MOBILE_BUTTON + marker, 1)
            print('  + Added TOC mobile button')

    # 4. Add the setupMobileTOC function definition just before "function setupSelectionToolbar"
    if 'setupMobileTOC' not in html:
        marker = '  function setupSelectionToolbar() {'
        if marker in html:
            html = html.replace(marker, MOBILE_JS_FN + marker, 1)
            print('  + Added setupMobileTOC function')

    # 5. Call setupMobileTOC() in the init handler, right after setupSelectionToolbar()
    if 'setupMobileTOC();' not in html:
        marker = 'setupSelectionToolbar();'
        if marker in html:
            html = html.replace(marker, marker + '\n    setupMobileTOC();', 1)
            print('  + Wired setupMobileTOC into init')

    with open(path, 'w') as f:
        f.write(html)
    print(f'OK: {path}')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'\nProcessing {p}')
        inject(p)
