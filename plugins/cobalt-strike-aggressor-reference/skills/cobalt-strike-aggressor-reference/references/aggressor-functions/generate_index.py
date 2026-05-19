#!/usr/bin/env python3
"""
Generate an alphabetical index of all Aggressor functions
"""

from pathlib import Path

def main():
    """Generate index of all function files."""
    functions_dir = Path("/Users/xpn/.claude/skills/skills/aggressor/references/aggressor-functions")
    
    # Get all markdown files except README and this script
    md_files = sorted([f for f in functions_dir.glob("*.md") if f.name != "README.md" and f.name != "INDEX.md"])
    
    # Group by first character
    grouped = {}
    for md_file in md_files:
        func_name = md_file.stem
        first_char = func_name[0].upper() if func_name[0].isalpha() else '#'
        
        if first_char not in grouped:
            grouped[first_char] = []
        grouped[first_char].append(func_name)
    
    # Generate index markdown
    index_content = ["# Alphabetical Index of Aggressor Functions\n"]
    index_content.append(f"Total functions: {len(md_files)}\n\n")
    
    # Add quick navigation
    index_content.append("## Quick Navigation\n\n")
    for char in sorted(grouped.keys()):
        index_content.append(f"[{char}](#{char.lower()}) | ")
    index_content.append("\n\n")
    
    # Add function listings
    for char in sorted(grouped.keys()):
        index_content.append(f"## {char}\n\n")
        for func_name in sorted(grouped[char]):
            index_content.append(f"- [{func_name}](./{func_name}.md)\n")
        index_content.append("\n")
    
    # Write index file
    index_path = functions_dir / "INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(''.join(index_content))
    
    print(f"Generated INDEX.md with {len(md_files)} functions")
    print(f"Functions grouped into {len(grouped)} categories")

if __name__ == "__main__":
    main()
