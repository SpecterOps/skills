#!/usr/bin/env python3
"""
Convert Sleep function documentation from HTML to clean Markdown
"""

import re
import os
from pathlib import Path
from html.parser import HTMLParser

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.current_text = []
        self.in_synopsis = False
        self.in_param = False
        self.in_example = False
        self.in_output = False
        self.in_link = False
        self.link_text = ""
        self.link_href = ""
        self.list_level = 0
        self.in_list_item = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'h1':
            pass  # Skip, we already have the title
        elif tag == 'h2':
            self.current_text.append('\n## ')
        elif tag == 'h3':
            self.current_text.append('\n### ')
        elif tag == 'span' and attrs_dict.get('class') == 'synopsis':
            self.in_synopsis = True
            self.current_text.append('\n```sleep\n')
        elif tag == 'span' and attrs_dict.get('class') == 'param':
            self.in_param = True
            self.current_text.append('`')
        elif tag == 'span' and attrs_dict.get('class') == 'function':
            pass  # Handle the link inside
        elif tag == 'p' and attrs_dict.get('class') == 'example':
            self.in_example = True
            self.current_text.append('\n```sleep\n')
        elif tag == 'p' and attrs_dict.get('class') == 'output':
            self.in_output = True
            self.current_text.append('\n**Output:**\n```\n')
        elif tag == 'a':
            self.in_link = True
            self.link_href = attrs_dict.get('href', '')
            self.link_text = ""
        elif tag == 'ul':
            self.list_level += 1
            self.current_text.append('\n')
        elif tag == 'li':
            self.in_list_item = True
            self.current_text.append('- ')
        elif tag == 'code':
            self.current_text.append('`')
        elif tag == 'pre':
            self.current_text.append('\n```\n')
        elif tag == 'br':
            self.current_text.append('\n')

    def handle_endtag(self, tag):
        if tag == 'span' and self.in_synopsis:
            self.in_synopsis = False
            self.current_text.append('\n```\n')
        elif tag == 'span' and self.in_param:
            self.in_param = False
            self.current_text.append('`')
        elif tag == 'p' and self.in_example:
            self.in_example = False
            self.current_text.append('\n```\n')
        elif tag == 'p' and self.in_output:
            self.in_output = False
            self.current_text.append('\n```\n')
        elif tag == 'a' and self.in_link:
            self.in_link = False
            # Convert HTML links to markdown, remove .html extension
            if self.link_href:
                func_name = self.link_href.replace('.html', '')
                self.current_text.append(f'[{self.link_text}]({func_name}.md)')
            else:
                self.current_text.append(self.link_text)
        elif tag == 'h2' or tag == 'h3':
            self.current_text.append('\n')
        elif tag == 'ul':
            self.list_level -= 1
        elif tag == 'li':
            self.in_list_item = False
            self.current_text.append('\n')
        elif tag == 'code':
            self.current_text.append('`')
        elif tag == 'pre':
            self.current_text.append('\n```\n')

    def handle_data(self, data):
        # Skip if it's just whitespace/newlines and we're not in text mode
        if data.strip() or self.in_example or self.in_output:
            if self.in_link:
                self.link_text += data
            else:
                # Clean up excessive whitespace but preserve intentional spacing
                if self.in_example or self.in_output:
                    self.current_text.append(data)
                else:
                    cleaned = ' '.join(data.split())
                    if cleaned:
                        self.current_text.append(cleaned)

    def handle_comment(self, data):
        # Skip HTML comments
        pass

    def get_markdown(self):
        result = ''.join(self.current_text)
        # Clean up multiple newlines
        result = re.sub(r'\n{3,}', '\n\n', result)
        # Clean up spaces before newlines
        result = re.sub(r' +\n', '\n', result)
        return result.strip()

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

        header = parts[0] + '---'
        html_content = parts[1]

        # Parse HTML to Markdown
        parser = HTMLToMarkdown()
        parser.feed(html_content)
        markdown_content = parser.get_markdown()

        # Combine header and markdown
        new_content = header + '\n\n' + markdown_content + '\n'

        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"  ✗ Error converting {filepath.name}: {e}")
        return False

def main():
    print("Converting Sleep function documentation from HTML to Markdown")
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
