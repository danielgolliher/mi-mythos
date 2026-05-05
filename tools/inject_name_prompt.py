#!/usr/bin/env python3
"""Inject the 'set your name' prompt into a brief. Idempotent."""
import sys

CSS = """  .comments-name-prompt {
    padding: 12px 14px;
    background: #fff7e0;
    border-bottom: 1px solid var(--rule);
    font-size: 12px;
    color: #5a4500;
    line-height: 1.5;
  }
  .comments-name-prompt[hidden] { display: none; }
  .comments-name-prompt p { margin: 0; }
  .comments-name-prompt strong { font-weight: 600; color: var(--ink); }
  .comments-name-prompt .name-prompt-trigger {
    background: transparent;
    border: none;
    color: var(--accent);
    font-weight: 600;
    font-family: inherit;
    font-size: inherit;
    padding: 0;
    cursor: pointer;
    text-decoration: underline;
  }
  .comments-name-prompt .name-prompt-trigger:hover { color: #8c4f25; }
"""

PROMPT_HTML = """  <div class="comments-name-prompt" id="name-prompt" hidden>
    <p>👋 Your comments will show up as <strong id="name-prompt-default">Commenter</strong>. <button class="name-prompt-trigger" id="name-prompt-trigger" type="button">Give yourself a name</button> so others can recognize you.</p>
  </div>
"""

JS_FN = """  function updateNamePrompt() {
    const u = getUser();
    const prompt = document.getElementById('name-prompt');
    const defaultLabel = document.getElementById('name-prompt-default');
    if (!prompt) return;
    if (u.name) {
      prompt.hidden = true;
    } else {
      prompt.hidden = false;
      if (defaultLabel) defaultLabel.textContent = u.defaultLabel;
    }
  }

"""

def inject(path):
    with open(path) as f: html = f.read()
    if 'comments-name-prompt' in html and 'updateNamePrompt' in html:
        print(f'  already injected, skipping: {path}')
        return

    # 1. CSS: insert before the .comments-empty block (which sits in the comments-system CSS)
    css_marker = '  .comments-empty {'
    if css_marker in html and 'comments-name-prompt' not in html:
        html = html.replace(css_marker, CSS + css_marker, 1)
        print('  + Added prompt CSS')

    # 2. HTML: insert the prompt right after the identity-edit form (just before #comments-list)
    html_marker = '  <div id="comments-list"></div>'
    if html_marker in html and 'id="name-prompt"' not in html:
        html = html.replace(html_marker, PROMPT_HTML + html_marker, 1)
        print('  + Added prompt HTML')

    # 3. JS function definition: just before setupMobileTOC (or setupRename if present)
    js_marker = '  function setupRename() {'
    if js_marker in html and 'updateNamePrompt' not in html:
        html = html.replace(js_marker, JS_FN + js_marker, 1)
        print('  + Added updateNamePrompt function')

    # 4. Wire trigger button to existing rename flow + call updateNamePrompt() on init
    #    Insert handler at the END of setupRename() — before the closing brace of the function.
    if "document.getElementById('name-prompt-trigger')" not in html:
        # Find the last line of setupRename() body (the closing brace after the keydown handler)
        old = "    nameInput.addEventListener('keydown', function(e) {\n      if (e.key === 'Escape') { e.preventDefault(); closeEdit(); }\n    });\n  }"
        new = """    nameInput.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') { e.preventDefault(); closeEdit(); }
    });
    const trigger = document.getElementById('name-prompt-trigger');
    if (trigger) trigger.addEventListener('click', openEdit);
  }"""
        if old in html:
            html = html.replace(old, new, 1)
            print('  + Wired prompt trigger into setupRename')

    # 5. Also make sure the rename form's submit handler refreshes the prompt
    #    The submit handler ends with `renderAll(fresh);` — append updateNamePrompt() there
    if "    editForm.addEventListener('submit', async function(e) {" in html:
        old2 = """      const fresh = await loadComments();
      renderAll(fresh);
    });"""
        new2 = """      const fresh = await loadComments();
      renderAll(fresh);
      updateNamePrompt();
    });"""
        if old2 in html and 'updateNamePrompt();\n    });' not in html:
            html = html.replace(old2, new2, 1)
            print('  + Hooked updateNamePrompt into rename-submit')

    # 6. Call updateNamePrompt() on init (in DOMContentLoaded, right after setupRename())
    if 'setupRename();\n    updateNamePrompt();' not in html:
        old3 = """    setupSelectionToolbar();
    setupMobileTOC();
    setupRename();"""
        new3 = """    setupSelectionToolbar();
    setupMobileTOC();
    setupRename();
    updateNamePrompt();"""
        if old3 in html:
            html = html.replace(old3, new3, 1)
            print('  + Called updateNamePrompt on init')

    with open(path, 'w') as f: f.write(html)
    print(f'OK: {path}')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'\nProcessing {p}')
        inject(p)
