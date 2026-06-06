from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Restore modal button link behavior
modal_replacement = (
    "document.getElementById('mBody').innerHTML = p.body + `\n"
    "    <hr class=\"m-divider\" />\n"
    "    <div style=\"display:flex;justify-content:flex-end\">\n"
    "      <a href=\"${p.drive}\" target=\"_blank\" rel=\"noopener\" class=\"drive-btn\">\n"
    "        <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z\"/><path d=\"M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z\"/><path d=\"M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z\"/><path d=\"M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z\"/></svg>\n"
    "        Xem bản đầy đủ\n"
    "      </a>\n"
    "    </div>`;"
)
text = re.sub(
    r"document\.getElementById\('mBody'\)\.innerHTML = p\.body;",
    modal_replacement,
    text,
    count=1,
)

projects_match = re.search(r"(const projects = \[)([\s\S]*?)(\];)", text)
if not projects_match:
    raise SystemExit('Could not find projects array')

projects_block = projects_match.group(2)
project_pattern = re.compile(
    r"id: '([^']*)',\s*num: '([^']*)',\s*tag: '([^']*)',\s*title: '([^']*)',\s*short: '([^']*)',\s*drive: '([^']*)',",
    re.MULTILINE,
)

projects = []
for m in project_pattern.finditer(projects_block):
    projects.append({
        'id': m.group(1),
        'num': m.group(2),
        'tag': m.group(3),
        'title': m.group(4),
        'short': m.group(5),
        'drive': m.group(6),
    })

if len(projects) == 0:
    raise SystemExit('No projects found')

new_projects = ['const projects = [']
for proj in projects:
    new_projects.append('      {')
    new_projects.append(f"        id: '{proj['id']}', num: '{proj['num']}',")
    new_projects.append(f"        tag: '{proj['tag']}',")
    new_projects.append(f"        title: '{proj['title']}',")
    new_projects.append(f"        short: '{proj['short']}',")
    new_projects.append(f"        drive: '{proj['drive']}',")
    new_projects.append(f"        body: `<p>{proj['short']}</p>`")
    new_projects.append('      },')
new_projects.append('    ];')
new_projects_text = '\n'.join(new_projects)

text = text[:projects_match.start(1)] + new_projects_text + text[projects_match.end(3):]
path.write_text(text, encoding='utf-8')
print(f'Restored {len(projects)} projects and modal link behavior')
