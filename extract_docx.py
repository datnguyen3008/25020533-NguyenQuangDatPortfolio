from docx import Document
from pathlib import Path
import html

docs = {
    'm1': Path(r'C:\Users\Lenovo\Documents\baitaplms1.docx'),
    'm2': Path(r'C:\Users\Lenovo\Documents\baitaplms2.docx'),
    'm3': Path(r'C:\Users\Lenovo\Documents\btlms3.docx'),
    'm4': Path(r'C:\Users\Lenovo\Documents\btlms4.docx'),
    'm5': Path(r'C:\Users\Lenovo\Documents\btlms5.docx'),
    'm6': Path(r'C:\Users\Lenovo\Documents\btlms6.docx'),
}

out = []
for key, path in docs.items():
    doc = Document(path)
    parts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            parts.append(html.escape(text))
    out.append(f'--- {key} {path.name}')
    for p in parts:
        out.append(p)
    out.append('')

out_path = Path('e:/bt portfolio/doc_contents.txt')
out_path.write_text('\n'.join(out), encoding='utf-8')
print('wrote', out_path)
