from pathlib import Path
import html
import re

index_path = Path(r'e:\bt portfolio\index.html')
doc_path = Path(r'e:\bt portfolio\doc_contents.txt')
text = index_path.read_text(encoding='utf-8')
raw = doc_path.read_text(encoding='utf-8').splitlines()

projects = {}
current = None
for line in raw:
    if line.startswith('--- '):
        parts = line.split(' ')
        if len(parts) >= 2:
            current = parts[1].strip()
            projects[current] = []
        else:
            current = None
    elif current is not None:
        projects[current].append(line)

if len(projects) != 6:
    raise SystemExit(f'Expected 6 project sections, got {len(projects)}')

replacements = {}
for key, lines in projects.items():
    html_lines = ['<div class="doc-content">']
    for line in lines:
        if not line.strip():
            html_lines.append('<br>')
            continue
        unescaped = html.unescape(line)
        clean = html.escape(unescaped)
        # Emphasize headings and numbered steps
        if unescaped.strip().startswith(('BÀI TẬP', 'BÁO CÁO', 'BÁO CÁO THỰC HÀNH', 'Họ và tên', 'I.', 'II.', 'III.', 'IV.', 'V.', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', 'III.', 'IV.', 'V.', 'KHẢO SÁT', 'I.Lựa', 'II.')):
            html_lines.append(f'<p><strong>{clean}</strong></p>')
        else:
            html_lines.append(f'<p>{clean}</p>')
    html_lines.append('</div>')
    body_html = '\n'.join(html_lines)
    replacements[key] = body_html

# Replace each body block in the index.html
for key, body_html in replacements.items():
    pattern = re.compile(
        r"(id: '%s',[\s\S]*?body: `)([\s\S]*?)(`[\s\S]*?\n\s*\},)" % key
    )
    def repl(match):
        return match.group(1) + body_html + match.group(3)
    if not pattern.search(text):
        raise SystemExit(f'Could not find project {key}')
    text = pattern.sub(repl, text, count=1)

# Remove the drive button from modal
text = text.replace(
    "document.getElementById('mBody').innerHTML = p.body + `\n    <hr class=\"m-divider\" />\n    <div style=\"display:flex;justify-content:flex-end\">\n      <a href=\"${p.drive}\" target=\"_blank\" rel=\"noopener\" class=\"drive-btn\">\n        <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z\"/><path d=\"M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z\"/><path d=\"M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z\"/><path d=\"M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z\"/></svg>\n        Xem bản đầy đủ\n      </a>\n    </div>`;",
    "document.getElementById('mBody').innerHTML = p.body;"
)

# Update section subtitle to reflect inline content display
text = text.replace(
    'Nội dung dự án được cập nhật theo 6 bài tập từ các file Word <strong>baitaplms1.docx</strong> đến <strong>btlms6.docx</strong>. Nhấn vào thẻ để xem chi tiết và liên kết Google Drive.',
    'Nội dung dự án được cập nhật theo 6 bài tập từ các file Word. Nhấn vào thẻ để xem nội dung đầy đủ ngay trên trang.'
)

index_path.write_text(text, encoding='utf-8')
print('index.html updated')
