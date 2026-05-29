#!/usr/bin/env python3
"""
Convert Sleep function documentation from HTML to clean Markdown (Version 2)
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_html(html_content):
    """Convert HTML to clean Markdown using BeautifulSoup"""
    soup = BeautifulSoup(html_content, 'html.parser')

    markdown_parts = []

    # Find the main content (skip head)
    body = soup.find('body')
    if not body:
        body = soup

    # Skip the first h1 (it's the title, already in header)
    h1 = body.find('h1')
    if h1 and hasattr(h1, 'decompose'):
        h1.decompose()

    # Process each main section
    elements = body.find_all(['h2', 'h3', 'p', 'ul', 'pre', 'span'], recursive=False) if hasattr(body, 'find_all') else []
    for element in elements:
        if element.name == 'h2':
            markdown_parts.append(f"\n## {element.get_text().strip()}\n")

        elif element.name == 'h3':
            markdown_parts.append(f"\n### {element.get_text().strip()}\n")

        elif element.name == 'span' and 'synopsis' in element.get('class', []):
            code = element.get_text().strip()
            markdown_parts.append(f"\n```sleep\n{code}\n```\n")

        elif element.name == 'p':
            classes = element.get('class', [])

            if 'synopsis' in classes:
                # Synopsis in a paragraph
                code = element.get_text().strip()
                markdown_parts.append(f"\n```sleep\n{code}\n```\n")

            elif 'example' in classes:
                # Example code
                code = element.get_text().strip()
                markdown_parts.append(f"\n**Example:**\n```sleep\n{code}\n```\n")

            elif 'output' in classes:
                # Output
                output = element.get_text().strip()
                markdown_parts.append(f"\n**Output:**\n```\n{output}\n```\n")

            else:
                # Regular paragraph - handle inline spans
                text = process_inline_elements(element)
                if text.strip():
                    markdown_parts.append(f"\n{text}\n")

        elif element.name == 'ul':
            # Process list
            for li in element.find_all('li', recursive=False):
                item_text = process_inline_elements(li)
                markdown_parts.append(f"- {item_text}\n")
            markdown_parts.append("\n")

        elif element.name == 'pre':
            code = element.get_text().strip()
            markdown_parts.append(f"\n```\n{code}\n```\n")

    # Join and clean up
    markdown = ''.join(markdown_parts)

    # Clean up excessive newlines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()

def process_inline_elements(element):
    """Process inline elements within a block element"""
    result = []

    for content in element.children:
        if isinstance(content, str):
            result.append(content)
        elif content.name == 'span':
            classes = content.get('class', [])
            if 'param' in classes:
                result.append(f"`{content.get_text()}`")
            elif 'function' in classes:
                # Handle function links
                link = content.find('a')
                if link:
                    func_name = link.get_text().strip()
                    href = link.get('href', '')
                    if href:
                        href = href.replace('.html', '.md')
                        result.append(f"[{func_name}]({href})")
                    else:
                        result.append(func_name)
                else:
                    result.append(content.get_text())
            else:
                result.append(content.get_text())
        elif content.name == 'a':
            text = content.get_text().strip()
            href = content.get('href', '')
            if href:
                href = href.replace('.html', '.md')
                result.append(f"[{text}]({href})")
            else:
                result.append(text)
        elif content.name == 'code':
            result.append(f"`{content.get_text()}`")
        elif content.name == 'br':
            result.append('\n')
        elif content.name:
            # Other tags, just get text
            result.append(content.get_text())

    text = ''.join(result)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text

def convert_file(filepath):
    """Convert a single file from HTML to Markdown"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract the header (everything before the HTML)
        parts = content.split('---', 1)
        if len(parts) < 2:
            print(f"  ⚠ Skipping {filepath.name} - no header found")
            return False

        header = parts[0].strip() + '\n\n---'
        html_content = parts[1]

        # Convert HTML to Markdown
        markdown_content = clean_html(html_content)

        # Combine header and markdown
        new_content = header + '\n\n' + markdown_content + '\n'

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"  ✗ Error converting {filepath.name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Converting Sleep function documentation from HTML to Markdown (v2)")
    print("=" * 70)

    # Get all .md files except the special ones
    skip_files = {'INDEX.md', 'README.md', 'SUMMARY.md', 'QUICKREF.md', 'intro.md'}
    md_files = [f for f in Path('.').glob('*.md') if f.name not in skip_files]

    print(f"Found {len(md_files)} function files to convert\n")

    success = 0
    failed = 0

    for filepath in sorted(md_files):
        print(f"Converting {filepath.name}...", end=' ')
        if convert_file(filepath):
            print("✓")
            success += 1
        else:
            print("✗")
            failed += 1

    print("\n" + "=" * 70)
    print(f"Complete! Success: {success}, Failed: {failed}")

    if success > 0:
        print(f"\n✓ {success} files converted to clean Markdown format")

if __name__ == "__main__":
    main()
