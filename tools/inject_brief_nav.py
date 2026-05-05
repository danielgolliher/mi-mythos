#!/usr/bin/env python3
"""Inject the cross-brief navigation strip. Idempotent.

To add a new example brief, append it to EXAMPLES below and re-run this
script over every brief in mi-mythos/examples/*/index.html.
"""
import sys, re

# Single source of truth for the example list. Order = display order.
EXAMPLES = [
    ('electronic-rent-payments', 'Electronic rent payments'),
    ('teacher-cba-student-outcomes', 'Teacher contracts &amp; student outcomes'),
]

CSS = """  /* === BRIEF NAVIGATION STRIP === */
  .brief-nav {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 12px;
    color: var(--muted);
    padding: 8px 0 12px;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--rule);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 4px 12px;
    line-height: 1.5;
  }
  .brief-nav .home-link {
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 11px;
  }
  .brief-nav .home-link:hover { text-decoration: underline; }
  .brief-nav .nav-divider { color: var(--rule); }
  .brief-nav .nav-label {
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 11px;
  }
  .brief-nav a.example-link {
    color: var(--ink);
    text-decoration: none;
    border-bottom: 1px dotted var(--accent);
    padding-bottom: 1px;
  }
  .brief-nav a.example-link:hover {
    color: var(--accent);
    background: rgba(107, 52, 16, 0.06);
  }
  .brief-nav .example-current {
    font-weight: 600;
    color: var(--ink);
    border-bottom: none;
    cursor: default;
  }
  @media (max-width: 600px) {
    .brief-nav { font-size: 12px; gap: 4px 10px; }
    .brief-nav .home-link, .brief-nav .nav-label { font-size: 10px; }
  }
"""

def build_nav_html():
    items = []
    for slug, title in EXAMPLES:
        items.append(f'<a class="example-link" href="../{slug}/" data-slug="{slug}">{title}</a>')
    items_html = '\n  <span class="nav-divider">·</span>\n  '.join(items)
    return f"""<nav class="brief-nav" aria-label="Other example briefs">
  <a href="../../" class="home-link">&larr; MI Mythos</a>
  <span class="nav-divider">&middot;</span>
  <span class="nav-label">Briefs:</span>
  {items_html}
</nav>
<script>
(function() {{
  var m = location.pathname.match(/\\/examples\\/([^/]+)\\//);
  if (!m) return;
  document.querySelectorAll('.brief-nav a.example-link').forEach(function(a) {{
    if (a.dataset.slug === m[1]) {{
      a.classList.add('example-current');
      a.removeAttribute('href');
    }}
  }});
}})();
</script>

"""

NAV_HTML = build_nav_html()

CSS_MARKER_PRE = '  /* Floating TOC sidebar */'  # CSS goes right before the floating TOC block

HTML_MARKER_PRE = '<div class="print-row">'  # nav goes right before the print row inside .wrap

def inject(path):
    with open(path) as f:
        html = f.read()

    # 1. CSS: insert just before the floating TOC sidebar block
    if 'BRIEF NAVIGATION STRIP' in html:
        # Replace existing block to allow updates (e.g. when a new example is added we'd need a re-render
        # ... but actually CSS is static; we leave it. Still, refresh the HTML below.)
        print('  · CSS already present, skipping')
    else:
        if CSS_MARKER_PRE in html:
            html = html.replace(CSS_MARKER_PRE, CSS + CSS_MARKER_PRE, 1)
            print('  + CSS injected')
        else:
            print('  ! CSS marker not found')

    # 2. HTML: insert just before <div class="print-row"> (the very first one inside .wrap)
    #    ALWAYS replace the existing nav so we can update the example list.
    pat = re.compile(r'<nav class="brief-nav"[\s\S]*?</script>\s*\n', re.MULTILINE)
    if pat.search(html):
        html = pat.sub(NAV_HTML, html, count=1)
        print('  ↻ Nav HTML re-rendered with current EXAMPLES list')
    else:
        if HTML_MARKER_PRE in html:
            # Insert nav before the FIRST occurrence of print-row inside .wrap
            html = html.replace(HTML_MARKER_PRE, NAV_HTML + HTML_MARKER_PRE, 1)
            print('  + Nav HTML injected')
        else:
            print('  ! print-row marker not found')

    with open(path, 'w') as f: f.write(html)
    print(f'OK: {path}')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'\nProcessing {p}')
        inject(p)
