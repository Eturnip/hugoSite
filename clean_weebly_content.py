#!/usr/bin/env python3
"""
Remove problematic Weebly video/image HTML from posts
"""
import re
from pathlib import Path

def clean_weebly_content(content):
    """Remove Weebly video and image gallery HTML"""
    
    # Remove <div class="wsite-video">...</div> blocks
    content = re.sub(r'<div\s+class="wsite-video"[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove wsite-image blocks
    content = re.sub(r'<div\s+class="wsite-image[^"]*"[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove <table> blocks that were part of embedded content
    content = re.sub(r'<table\s+[^>]*class="[^"]*image[^"]*"[^>]*>.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    return content

def process_file(file_path):
    """Clean a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="wsite-video"' not in content and '<div class="wsite-image' not in content:
        return False, "No Weebly content found"
    
    cleaned = clean_weebly_content(content)
    
    if cleaned != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return True, f"Cleaned {file_path.name}"
    
    return False, "No changes made"

def main():
    post_dir = Path("content/post")
    
    # Posts we know have problematic Weebly content
    problem_files = [
        "2020-11-30-422.md",  # The failing one with video
        "2020-11-23-421.md",  # Has Weebly gallery
    ]
    
    cleaned_count = 0
    for filename in problem_files:
        file_path = post_dir / filename
        if not file_path.exists():
            print(f"⚠ File not found: {filename}")
            continue
        
        success, message = process_file(file_path)
        if success:
            print(f"✓ {message}")
            cleaned_count += 1
        else:
            print(f"ℹ {filename}: {message}")
    
    print(f"\nCleaned: {cleaned_count} files")

if __name__ == "__main__":
    main()
