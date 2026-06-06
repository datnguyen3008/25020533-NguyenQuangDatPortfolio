import re
from pathlib import Path
from docx import Document
import html

index_path = Path(r'e:\bt portfolio\index.html')
docs = {
    'm1': Path(r'C:\Users\Lenovo\Documents\baitaplms1.docx'),
    'm2': Path(r'C:\Users\Lenovo\Documents\baitaplms2.docx'),
    'm3': Path(r'C:\Users\Lenovo\Documents\btlms3.docx'),
    'm4': Path(r'C:\Users\Lenovo\Documents\btlms4.docx'),
    'm5': Path(r'C:\Users\Lenovo\Documents\btlms5.docx'),
    'm6': Path(r'C:\Users\Lenovo\Documents\btlms6.docx'),
}

text = index_path.read_text(encoding='utf-8')

for key, path in docs.items():
    doc = Document(path)
    parts = []
    for para in doc.paragraphs:
        line = para.text.strip()
        if line:
            parts.append(html.escape(line))
    html_lines = ['<div class="doc-content">']
    for line in parts:
        html_lines.append(f'  <p>{line}</p>')
    html_lines.append('</div>')
    new_body = '\n'.join(html_lines)

    # Replace body string for this project
    pattern = re.compile(
        r"(id: '" + re.escape(key) + r"',[\s\S]*?body: `)([\s\S]*?)(`\s*\n\s*\}\s*(?:,|\]))",
        re.MULTILINE
    )
    if not pattern.search(text):
        raise SystemExit(f'Could not find project body for {key}')
    def repl(m):
        return m.group(1) + new_body + m.group(3)
    text = pattern.sub(repl, text, count=1)

# Also remove appended drive button from openModal
open_modal_pattern = re.compile(
    r"document\.getElementById\('mBody'\)\.innerHTML = p\.body \+ `[\s\S]*?`;",
    re.MULTILINE
)
text, n = open_modal_pattern.subn("document.getElementById('mBody').innerHTML = p.body;", text)
if n == 0:
    raise SystemExit('Could not replace openModal append section')

index_path.write_text(text, encoding='utf-8')
print('Updated index.html with embedded document contents')
