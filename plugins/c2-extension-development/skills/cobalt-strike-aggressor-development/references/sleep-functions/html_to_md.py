#!/usr/bin/env python3
"""
Simple HTML to Markdown converter for Sleep documentation
"""

import re
from pathlib import Path

def html_to_markdown(html):
    """Convert HTML to Markdown using regex replacements"""

    # Remove HTML/head/body tags
    html = re.sub(r'<html[^>]*>|</html>|<head>.*?</head>|<body[^>]*>|</body>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # Remove style and script tags
    html = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Skip first h1 (already in header)
    html = re.sub(r'<h1>.*?</h1>', '', html, count=1, flags=re.IGNORECASE | re.DOTALL)

    # Headers
    html = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<h4>(.*?)</h4>', r'\n#### \1\n', html, flags=re.IGNORECASE | re.DOTALL)

    # Synopsis spans
    html = re.sub(r'<span class="synopsis">(.*?)</span>', r'\n```sleep\n\1\n```\n', html, flags=re.IGNORECASE | re.DOTALL)

    # Example and output paragraphs
    html = re.sub(r'<p class="example">(.*?)</p>', r'\n**Example:**\n```sleep\n\1\n```\n', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<p class="output">(.*?)</p>', r'\n**Output:**\n```\n\1\n```\n', html, flags=re.IGNORECASE | re.DOTALL)

    # Parameter spans - convert to inline code
    html = re.sub(r'<span class="param">(.*?)</span>', r'`\1`', html, flags=re.IGNORECASE | re.DOTALL)

    # Function links
    def replace_function_link(match):
        content = match.group(1)
        # Extract href and text
        link_match = re.search(r'<a href="([^"]+)">(.*?)</a>', content, re.IGNORECASE)
        if link_match:
            href = link_match.group(1).replace('.html', '.md')
            text = link_match.group(2)
            # Clean up &amp;
            text = text.replace('&amp;', '&')
            return f'[{text}]({href})'
        return content

    html = re.sub(r'<span class="function">(.*?)</span>', replace_function_link, html, flags=re.IGNORECASE | re.DOTALL)

    # Regular links
    html = re.sub(r'<a href="([^"]+)">(.*?)</a>', lambda m: f'[{m.group(2)}]({m.group(1).replace(".html", ".md")})', html, flags=re.IGNORECASE)

    # Lists
    html = re.sub(r'<ul[^>]*>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</ul>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<li[^>]*>', '- ', html, flags=re.IGNORECASE)
    html = re.sub(r'</li>', '\n', html, flags=re.IGNORECASE)

    # Code blocks
    html = re.sub(r'<pre>(.*?)</pre>', r'\n```\n\1\n```\n', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<code>(.*?)</code>', r'`\1`', html, flags=re.IGNORECASE | re.DOTALL)

    # Paragraphs
    html = re.sub(r'<p[^>]*>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</p>', '\n', html, flags=re.IGNORECASE)

    # Line breaks
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)

    # Remove remaining HTML tags
    html = re.sub(r'<[^>]+>', '', html)

    # Clean up HTML entities
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&nbsp;', ' ')

    # Clean up whitespace
    html = re.sub(r' +', ' ', html)  # Multiple spaces to single
    html = re.sub(r'\n +', '\n', html)  # Space at start of line
    html = re.sub(r' +\n', '\n', html)  # Space at end of line
    html = re.sub(r'\n{3,}', '\n\n', html)  # Multiple newlines

    return html.strip()

def convert_file(filepath):
    """Convert a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split header and HTML
        parts = content.split('---', 1)
        if len(parts) < 2:
            return False

        header = parts[0].strip() + '\n\n---'
        html_content = parts[1]

        # Convert to markdown
        markdown = html_to_markdown(html_content)

        # Combine
        new_content = header + '\n\n' + markdown + '\n'

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("Converting Sleep documentation HTML to Markdown")
    print("=" * 70)

    skip_files = {'INDEX.md', 'README.md', 'SUMMARY.md', 'QUICKREF.md', 'intro.md'}
    files = [f for f in Path('.').glob('*.md') if f.name not in skip_files]

    print(f"Processing {len(files)} files...\n")

    success = failed = 0
    for f in sorted(files):
        if convert_file(f):
            success += 1
            print(f"✓ {f.name}")
        else:
            failed += 1
            print(f"✗ {f.name}")

    print(f"\n{'=' * 70}")
    print(f"Complete! Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()
