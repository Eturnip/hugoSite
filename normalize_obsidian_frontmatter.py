from pathlib import Path
import re

root = Path('content/post')
count = 0

for p in sorted(root.rglob('*.md')):
    text = p.read_text(encoding='utf-8', errors='surrogateescape')
    
    # Split frontmatter from content
    if not text.startswith('---'):
        continue
    
    parts = text.split('---', 2)
    if len(parts) < 3:
        continue
    
    fm_lines = parts[1].strip().split('\n')
    content = parts[2]
    
    # Parse frontmatter manually
    fm = {}
    current_key = None
    for line in fm_lines:
        if ':' in line and not line.startswith(' '):
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            current_key = key
            # Handle inline values
            if val.startswith('['):
                val = eval(val)
            fm[key] = val if val else None
        elif line.startswith('  - ') and current_key:
            # Handle list items
            item = line.strip()[2:].strip()
            if not isinstance(fm[current_key], list):
                fm[current_key] = []
            fm[current_key].append(item)
    
    # Build new frontmatter
    new_fm_lines = []
    
    # layout
    new_fm_lines.append('layout: post')
    
    # title
    if 'title' in fm:
        title = fm['title'].strip('"').strip("'") if fm['title'] else '""'
        new_fm_lines.append(f'title: "{title}"')
    
    # date - remove Z suffix
    if 'date' in fm:
        date_str = fm['date']
        if date_str and date_str.endswith('Z'):
            date_str = date_str[:-1]
        new_fm_lines.append(f'date: {date_str}')
    
    # categories - convert to single value
    if 'categories' in fm:
        cats = fm['categories']
        if isinstance(cats, list):
            cat_val = cats[0] if cats else 'Blog'
        else:
            cat_val = str(cats).strip('[]').strip().split(',')[0].strip().strip('"').strip("'")
        new_fm_lines.append(f'categories: {cat_val}')
    
    # tags - convert to YAML list format
    if 'tags' in fm:
        tags = fm['tags']
        if not isinstance(tags, list):
            if isinstance(tags, str):
                if tags.startswith('['):
                    tags = eval(tags)
                else:
                    tags = [tags]
        
        if isinstance(tags, list) and tags:
            new_fm_lines.append('tags:')
            for tag in tags:
                tag_str = str(tag).strip().lstrip('-').strip('[]').strip('"').strip("'").strip()
                if tag_str:
                    new_fm_lines.append(f'  - {tag_str}')
    
    # author
    if 'author' in fm and fm['author']:
        author = fm['author'].strip('"').strip("'")
        new_fm_lines.append(f'author: {author}')
    
    # description
    if 'description' in fm and fm['description'] and fm['description'].strip('"'):
        desc = fm['description'].strip('"').strip("'")
        new_fm_lines.append(f'description: {desc}')
    
    new_frontmatter = '---\n' + '\n'.join(new_fm_lines) + '\n---'
    new_text = new_frontmatter + content
    
    if new_text != text:
        p.write_text(new_text, encoding='utf-8', newline='')
        count += 1
        print(p.name)

print(f'\nCHANGED {count} files')
