#!/usr/bin/env python3
"""
Rename files with UTF-8 BOM in their filenames
"""
import subprocess
from pathlib import Path

def main():
    post_dir = Path("content/post")
    
    # Get list of files with BOM
    files_with_bom = []
    for file in post_dir.glob("*.md"):
        if '\ufeff' in file.name:
            files_with_bom.append(file)
    
    print(f"Found {len(files_with_bom)} files with BOM in filename")
    
    if not files_with_bom:
        print("No files to rename")
        return
    
    renamed_count = 0
    error_count = 0
    
    for old_path in files_with_bom:
        new_name = old_path.name.replace('\ufeff', '')
        new_path = old_path.parent / new_name
        
        try:
            # Use git mv to preserve history
            result = subprocess.run(
                ['git', 'mv', str(old_path), str(new_path)],
                capture_output=True,
                text=True,
                cwd='.'
            )
            
            if result.returncode == 0:
                print(f"✓ Renamed: {old_path.name} -> {new_name}")
                renamed_count += 1
            else:
                print(f"✗ Error renaming {old_path.name}: {result.stderr}")
                error_count += 1
        except Exception as e:
            print(f"✗ Exception renaming {old_path.name}: {e}")
            error_count += 1
    
    print(f"\n{'-'*60}")
    print(f"Successfully renamed: {renamed_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    main()
