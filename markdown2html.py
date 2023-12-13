#!/usr/bin/python3
"""Markdown to HTML converter module"""
import sys
import os

def markdown_to_html(line):
    # Determining the level of the heading
    heading_level = 0
    while line.startswith('#'):
        heading_level += 1
        line = line[1:]

    # Removing leading and trailing spaces
    line = line.strip()

    # Converting to HTML
    if heading_level > 0:
        return f"<h{heading_level}>{line}</h{heading_level}>"
    else:
        return line

def main():
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Assigning file names to variables
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Reading Markdown file and writing to HTML file
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            html_line = markdown_to_html(line)
            html_file.write(html_line + '\n')

    sys.exit(0)

if __name__ == "__main__":
    main()