from pathlib import Path
import re

root = Path(r'c:/github/hugoSite/content/post')
count = 0

for p in sorted(root.rglob('*.md')):
    text = p.read_text(encoding='utf-8', errors='surrogateescape')
    new = text
    new = re.sub(r'(?m)^tag:\s*[-\s]*Best\s*[_ ]?Games\s*$', 'tag: Best_Games', new)
    new = re.sub(r'(?m)^tags:\s*\[\s*["\']?\s*[-\s]*Best\s*[_ ]?Games\s*["\']?\s*\]\s*$', 'tags: ["Best_Games"]', new)
    if new != text:
        p.write_text(new, encoding='utf-8', newline='')
        count += 1
        print(p)

print(f'CHANGED {count} files')
