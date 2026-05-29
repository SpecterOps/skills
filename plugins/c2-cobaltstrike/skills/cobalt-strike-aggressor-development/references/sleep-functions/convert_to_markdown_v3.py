#!/usr/bin/env python3
"""
Convert Sleep function documentation from HTML to clean Markdown (Version 3)
Uses html.parser (built-in) instead of BeautifulSoup
"""

import re
from pathlib import Path
from html.parser import HTMLParser

class SleepHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.current_section = None
        self.in_synopsis = False
        self.in_param = False
        self.in_example = False
        self.in_output = False
        self.in_function_link = False
        self.in_list = False
        self.in_pre = False
        self.link_text = ""
        self.link_href = ""
        self.skip_h1 = True
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'h1':
            self.skip_h1 = True
            return

        elif tag == 'h2':
            self.flush_buffer()
            self.current_section = ""

        elif tag == 'h3':
            self.flush_buffer()
            self.current_section = "###"

        elif tag == 'span':
            class_name = attrs_dict.get('class', '')
            if class_name == 'synopsis':
                self.flush_buffer()
                self.in_synopsis = True
                self.output.append('\n```sleep\n')
            elif class_name == 'param':
                self.in_param = True
                self.buffer.append('`')
            elif class_name == 'function':
                self.in_function_link = True

        elif tag == 'p':
            class_name = attrs_dict.get('class', '')
            if class_name == 'example':
                self.flush_buffer()
                self.in_example = True
                self.output.append('\n**Example:**\n```sleep\n')
            elif class_name == 'output':
                self.flush_buffer()
                self.in_output = True
                self.output.append('\n**Output:**\n```\n')
            else:
                self.flush_buffer()

        elif tag == 'a':
            self.link_href = attrs_dict.get('href', '')
            self.link_text = ""

        elif tag == 'ul':
            self.flush_buffer()
            self.in_list = True
            self.output.append('\n')

        elif tag == 'li':
            self.buffer.append('- ')

        elif tag == 'pre':
            self.flush_buffer()
            self.in_pre = True
            self.output.append('\n```\n')

        elif tag == 'code':
            self.buffer.append('`')

        elif tag == 'br':
            self.buffer.append('\n')

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.skip_h1 = False

        elif tag == 'h2':
            text = ''.join(self.buffer).strip()
            self.output.append(f'\n## {text}\n')
            self.buffer = []
            self.current_section = None

        elif tag == 'h3':
            text = ''.join(self.buffer).strip()
            self.output.append(f'\n### {text}\n')
            self.buffer = []
            self.current_section = None

        elif tag == 'span':
            if self.in_synopsis:
                self.output.append('\n```\n')
                self.in_synopsis = False
            elif self.in_param:
                self.buffer.append('`')
                self.in_param = False
            elif self.in_function_link:
                self.in_function_link = False

        elif tag == 'p':
            if self.in_example:
                self.output.append('\n```\n')
                self.in_example = False
            elif self.in_output:
                self.output.append('\n```\n')
                self.in_output = False
            else:
                self.flush_buffer()
                self.output.append('\n')

        elif tag == 'a':
            if self.link_href:
                href = self.link_href.replace('.html', '.md')
                self.buffer.append(f'[{self.link_text}]({href})')
            else:
                self.buffer.append(self.link_text)
            self.link_href = ""
            self.link_text = ""

        elif tag == 'li':
            self.flush_buffer()
            self.output.append('\n')

        elif tag == 'ul':
            self.in_list = False
            self.output.append('\n')

        elif tag == 'pre':
            self.output.append('\n```\n')
            self.in_pre = False

        elif tag == 'code':
            self.buffer.append('`')

    def handle_data(self, data):
        if self.skip_h1:
            return

        # Store link text separately
        if self.link_href:
            self.link_text += data
            return

        # For code blocks and output, preserve formatting
        if self.in_synopsis or self.in_example or self.in_output or self.in_pre:
            self.output.append(data)
        else:
            # Clean whitespace for regular text
            cleaned = data.strip()
            if cleaned:
                self.buffer.append(cleaned + ' ')

    def handle_comment(self, data):
        # Skip comments
        pass

    def flush_buffer(self):
        if self.buffer:
            text = ''.join(self.buffer).strip()
            if text:
                self.output.append(text + '\n')
            self.buffer = []

    def get_markdown(self):
        self.flush_buffer()
        result = ''.join(self.output)

        # Clean up excessive newlines
        result = re.sub(r'\n{3,}', '\n\n', result)
        # Clean up spaces
        result = re.sub(r' +', ' ', result)
        # Clean up space before newline
        result = re.sub(r' \n', '\n', result)

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

        header = parts[0].strip() + '\n\n---'
        html_content = parts[1]

        # Parse HTML to Markdown
        parser = SleepHTMLParser()
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
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Converting Sleep function documentation from HTML to Markdown (v3)")
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
