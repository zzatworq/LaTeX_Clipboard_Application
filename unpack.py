import os
import re
import argparse

def create_file_structure(input_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content by '###' delimiter
    sections = content.split('###')[1:]  # Skip the initial file tree or empty section

    # Process each section
    for section in sections:
        # Extract file path and content
        lines = section.strip().split('\n')
        if not lines:
            continue

        # First line after ### is the file path
        file_path = lines[0].strip()

        # Extract content, handling code block markers
        content_lines = lines[1:]
        if content_lines and content_lines[0].strip().startswith("'''python"):
            # Remove the opening and closing code block markers
            content_lines = content_lines[1:]  # Skip '''python
            if content_lines and content_lines[-1].strip() == "'''":
                content_lines = content_lines[:-1]  # Remove closing '''
        elif content_lines and content_lines[0].strip() == '```python':
            # Handle ``` code blocks
            content_lines = content_lines[1:]  # Skip ```python
            if content_lines and content_lines[-1].strip() == '```':
                content_lines = content_lines[:-1]  # Remove closing ```

        # Join the content
        file_content = '\n'.join(line.rstrip() for line in content_lines)

        # Create directories if they don't exist
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Write content to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Created file: {file_path}")
        except Exception as e:
            print(f"Error creating file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Create file structure from application.txt-like file")
    parser.add_argument('input_file', help="Path to the input file (e.g., application.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist")
        return

    create_file_structure(args.input_file)

if __name__ == "__main__":
    main()