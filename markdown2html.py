#!/usr/bin/python3
"""Markdown to HTML converter module"""
import sys
import os

def markdown_to_html(lines):
    html_lines = []
    in_list = False

    for line in lines:
        line = line.strip()

        if line.startswith('#'):
            # Handling headings
            heading_level = line.count('#')
            line = line.strip('# ')
            html_lines.append(f"<h{heading_level}>{line}</h{heading_level}>")
        elif line.startswith('- '):
            # Handling unordered list items
            if not in_list:
                in_list = True
                html_lines.append("<ul>")
            line = line.strip('- ')
            html_lines.append(f"<li>{line}</li>")
        else:
            if in_list:
                # Closing the list if it was open
                in_list = False
                html_lines.append("</ul>")
            html_lines.append(line)

    if in_list:
        # Close the list if it's still open at the end of file
        html_lines.append("</ul>")

    return '\n'.join(html_lines)

def main():
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
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