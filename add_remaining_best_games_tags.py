#!/usr/bin/env python3
"""
Add Best_Games tag to any posts that mention "best games" but don't have the tag
"""
import re
from pathlib import Path
import yaml

def process_markdown_file(file_path):
    """Add Best_Games tag if file has best games content but no tag"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid markdown format"
        
        frontmatter_str = parts[1]
        body = parts[2]
        
        # Check if "best games" appears in content (case-insensitive)
        if not re.search(r'best\s+games', body, re.IGNORECASE):
            return False, "No 'best games' found in content"
        
        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError as e:
            return False, f"YAML parse error: {e}"
        
        # Check if already has Best_Games tag
        tags = frontmatter.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags] if tags else []
        
        if "Best_Games" in tags:
            return False, "Already has Best_Games tag"
        
        # Add the tag
        tags.append("Best_Games")
        frontmatter['tags'] = tags
        
        # Rebuild the file
        new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content = f"---\n{new_frontmatter}---{body}"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"Added Best_Games tag to {file_path.name}"
    
    return False, "No frontmatter found"

def main():
    post_dir = Path("content/post")
    
    if not post_dir.exists():
        print(f"Error: {post_dir} does not exist")
        return
    
    files_to_process = [
        "2012-11-19-003.md",
        "2013-05-13-028.md",
        "2014-12-29-113.md",
        "2016-05-09-184.md",
        "2016-11-28-213.md",
        "2017-03-13-228.md",
        "2017-10-09-258.md",
        "2018-03-12-280.md",
        "2021-01-04-427.md",
        "2022-10-10-519.md",
        "2023-01-16-533.md",
        "2024-05-06-600.md",
        "2026-01-26-690.md",
    ]
    
    added_count = 0
    error_count = 0
    
    for filename in files_to_process:
        file_path = post_dir / filename
        if not file_path.exists():
            print(f"⚠ File not found: {filename}")
            error_count += 1
            continue
        
        success, message = process_markdown_file(file_path)
        if success:
            print(f"✓ {message}")
            added_count += 1
        else:
            print(f"✗ {filename}: {message}")
            error_count += 1
    
    print(f"\n{'-'*60}")
    print(f"Tags added: {added_count}")
    print(f"Errors/Skipped: {error_count}")

if __name__ == "__main__":
    main()
