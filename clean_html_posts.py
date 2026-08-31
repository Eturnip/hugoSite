#!/usr/bin/env python3
"""
Clean HTML tags from old blog posts and convert to clean markdown
"""
import re
from pathlib import Path
import html
import yaml

def clean_html_content(content):
    """Remove HTML tags and clean up content"""
    
    # Decode HTML entities
    content = html.unescape(content)
    
    # Remove style attributes from spans
    content = re.sub(r'<span[^>]*style="[^"]*"[^>]*>', '', content)
    
    # Remove empty spans
    content = re.sub(r'<span></span>', '', content)
    content = re.sub(r'<span>\s*</span>', '', content)
    
    # Remove remaining span tags
    content = re.sub(r'</?span[^>]*>', '', content)
    
    # Remove div tags but keep their content
    content = re.sub(r'<div[^>]*class="blog-content"[^>]*>', '', content)
    content = re.sub(r'<div[^>]*class="paragraph"[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)
    
    # Convert <br> to double newline for markdown paragraphs
    content = re.sub(r'<br\s*/?>\s*<br\s*/?>', '\n\n', content)
    content = re.sub(r'<br\s*/?>', '\n\n', content)
    
    # Clean up excessive whitespace but preserve paragraph breaks
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:  # Only add non-empty lines
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1] != '':  # Add single empty line for paragraph break
            cleaned_lines.append('')
    
    # Join and remove multiple consecutive empty lines
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content.strip()

def process_markdown_file(file_path):
    """Clean HTML from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has blog-content div
        if '<div class="blog-content">' not in content:
            return False, "No HTML structure found"
        
        # Split frontmatter and body
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, "Invalid frontmatter"
            
            frontmatter = parts[1]
            body = parts[2]
            
            # Clean the body content
            cleaned_body = clean_html_content(body)
            
            # Reconstruct the file
            new_content = f"---{frontmatter}---\n\n{cleaned_body}\n"
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, f"Cleaned {file_path.name}"
        else:
            return False, "No frontmatter found"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    post_dir = Path("content/post")
    
    if not post_dir.exists():
        print(f"Error: {post_dir} does not exist")
        return
    
    print("Searching for posts with HTML structure...")
    
    # Find all markdown files with blog-content div
    html_posts = []
    for post_file in post_dir.glob("*.md"):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<div class="blog-content">' in content:
                    html_posts.append(post_file)
        except Exception as e:
            print(f"Error reading {post_file.name}: {e}")
    
    print(f"Found {len(html_posts)} posts with HTML structure")
    
    if not html_posts:
        print("No posts to clean")
        return
    
    # Ask for confirmation
    response = input(f"\nClean {len(html_posts)} posts? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborted")
        return
    
    cleaned_count = 0
    error_count = 0
    
    for i, file_path in enumerate(html_posts, 1):
        success, message = process_markdown_file(file_path)
        
        if success:
            print(f"[{i}/{len(html_posts)}] ✓ {message}")
            cleaned_count += 1
        else:
            print(f"[{i}/{len(html_posts)}] ✗ {file_path.name}: {message}")
            error_count += 1
    
    print(f"\n{'-'*60}")
    print(f"Successfully cleaned: {cleaned_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {len(html_posts)}")

if __name__ == "__main__":
    main()
