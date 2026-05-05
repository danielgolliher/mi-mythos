#!/usr/bin/env python3
"""Inject the commenting CSS and HTML+JS into the LL 64 brief."""

BRIEF = '/Users/danielgolliher/projects/electronic-rent-payments/index.html'
CSS_FILE = '/tmp/comments-css.html'
HTMLJS_FILE = '/tmp/comments-htmljs.html'

with open(CSS_FILE) as f: css_block = f.read()
with open(HTMLJS_FILE) as f: htmljs_block = f.read()
with open(BRIEF) as f: html = f.read()

# CSS: insert right before "</style>" (last occurrence)
css_marker = "    .toc-top::after, blockquote a::after { content: \"\" !important; }\n  }\n</style>"
new_css_marker = "    .toc-top::after, blockquote a::after { content: \"\" !important; }\n  }\n" + css_block + "</style>"
assert css_marker in html, "CSS insertion marker not found"
html = html.replace(css_marker, new_css_marker, 1)

# HTML+JS: insert right after "</script>" and before "</body>"
js_marker = "</script>\n</body>"
new_js_marker = "</script>\n\n" + htmljs_block + "</body>"
assert js_marker in html, "JS insertion marker not found"
html = html.replace(js_marker, new_js_marker, 1)

with open(BRIEF, 'w') as f: f.write(html)
print("OK — inserted both blocks")
