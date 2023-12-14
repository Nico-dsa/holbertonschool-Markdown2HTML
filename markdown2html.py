#!/usr/bin/python3
"""Markdown to HTML converter module"""
import sys
import os
import re

def format_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

def markdown_to_html(lines):
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False
    paragraph = []

    def close_lists():
        nonlocal in_unordered_list, in_ordered_list
        if in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False
        if in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False

    def process_paragraph():
        if paragraph:
            html_lines.append("<p>")
            for p_line in paragraph:
                html_lines.append(format_text(p_line) + "<br />")
            html_lines[-1] = html_lines[-1].rstrip("<br />")  # Remove last <br />
            html_lines.append("</p>")
            paragraph.clear()

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith('#'):
            process_paragraph()
            close_lists()
            # Handling headings
            heading_level = stripped_line.count('#')
            stripped_line = stripped_line.strip('# ')
            html_lines.append(f"<h{heading_level}>{format_text(stripped_line)}</h{heading_level}>")
        elif stripped_line.startswith('- '):
            process_paragraph()
            if not in_unordered_list:
                in_unordered_list = True
                html_lines.append("<ul>")
            stripped_line = stripped_line.strip('- ')
            html_lines.append(f"<li>{format_text(stripped_line)}</li>")
        elif stripped_line.startswith('* '):
            process_paragraph()
            if not in_ordered_list:
                in_ordered_list = True
                html_lines.append("<ol>")
            stripped_line = stripped_line.strip('* ')
            html_lines.append(f"<li>{format_text(stripped_line)}</li>")
        elif stripped_line:
            if in_unordered_list or in_ordered_list:
                close_lists()
            paragraph.append(stripped_line)
        else:
            process_paragraph()
            close_lists()

    process_paragraph()

    return '\n'.join(html_lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as md_file:
        lines = md_file.readlines()

    html_content = markdown_to_html(lines)

    with open(output_file, 'w') as html_file:
        html_file.write(html_content)

    sys.exit(0)

if __name__ == "__main__":
    main()