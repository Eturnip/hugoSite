#!/usr/bin/env python3
"""
Test cleaning a single post to verify the script works correctly
"""
import re
import html
from pathlib import Path

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

def test_single_file():
    file_path = Path("content/post/2017-10-09-258.md")
    
    print(f"Testing on: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    # Split frontmatter and body
    if original.startswith('---'):
        parts = original.split('---', 2)
        frontmatter = parts[1]
        body = parts[2]
        
        print("\n" + "="*60)
        print("ORIGINAL BODY (first 500 chars):")
        print("="*60)
        print(body[:500])
        
        # Clean the body
        cleaned_body = clean_html_content(body)
        
        print("\n" + "="*60)
        print("CLEANED BODY (first 500 chars):")
        print("="*60)
        print(cleaned_body[:500])
        
        print("\n" + "="*60)
        print("FULL CLEANED CONTENT:")
        print("="*60)
        print(cleaned_body)

if __name__ == "__main__":
    test_single_file()
