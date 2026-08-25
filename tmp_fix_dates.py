from pathlib import Path
import re

root = Path('content/post')
count = 0
for p in sorted(root.rglob('*.md')):
    text = p.read_text(encoding='utf-8', errors='surrogateescape')
    new_lines = []
    changed = False
    for line in text.splitlines():
        m = re.match(r'^(date:\s*)(["\'])(.*?)(\2)\s*$', line)
        if m:
            new_lines.append(f"{m.group(1)}{m.group(3)}")
            changed = True
        else:
            new_lines.append(line)
    if changed:
        new_text = '\n'.join(new_lines)
        if text.endswith('\n'):
            new_text += '\n'
        p.write_text(new_text, encoding='utf-8', newline='')
        count += 1
        print(p)
print(f'CHANGED {count} files')
