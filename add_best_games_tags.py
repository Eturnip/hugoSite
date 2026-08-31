#!/usr/bin/env python3
"""
Add Best_Games tag to all posts that contain "Best Games -" in their content
"""
import os
import re
from pathlib import Path
import yaml

def process_markdown_file(file_path):
    """
    Add Best_Games tag to a markdown file if it contains "Best Games -" in content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split frontmatter from content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid markdown format"
        
        frontmatter_str = parts[1]
        body = parts[2]
        
        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError as e:
            return False, f"YAML parse error: {e}"
        
        # Check if "Best Games -" appears in the body
        if "Best Games -" not in body:
            return False, "No 'Best Games -' found in content"
        
        # Check if already has Best_Games tag
        tags = frontmatter.get('tags', [])
        if not isinstance(tags, list):
            tags = [tags] if tags else []
        
        if "Best_Games" in tags:
            return False, "Already has Best_Games tag"
        
        # Add the tag
        tags.append("Best_Games")
        frontmatter['tags'] = tags
        
        # Rebuild the file with updated frontmatter
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
    
    added_count = 0
    skipped_count = 0
    error_count = 0
    
    for md_file in sorted(post_dir.glob("*.md")):
        success, message = process_markdown_file(md_file)
        if success:
            print(f"✓ {message}")
            added_count += 1
        else:
            # Only print skipped if it's not an existing tag message
            if "Already has" not in message and "No 'Best Games -'" not in message:
                print(f"⚠ {md_file.name}: {message}")
                error_count += 1
            else:
                skipped_count += 1
    
    print(f"\n{'-'*60}")
    print(f"Total files processed: {added_count + skipped_count + error_count}")
    print(f"Tags added: {added_count}")
    print(f"Already tagged or no Best Games content: {skipped_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    main()
