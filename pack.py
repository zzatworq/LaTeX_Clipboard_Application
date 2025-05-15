import os
import argparse
from pathlib import Path
import pathspec

def load_gitignore(base_dir):
    """Load .gitignore patterns using pathspec"""
    gitignore_path = os.path.join(base_dir, '.gitignore')
    if not os.path.exists(gitignore_path):
        return None

    with open(gitignore_path, 'r', encoding='utf-8') as f:
        patterns = f.read().splitlines()

    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

def is_ignored(file_path, base_dir, spec):
    """Check if the file is ignored by the gitignore spec"""
    if spec is None:
        return False
    rel_path = os.path.relpath(file_path, base_dir)
    return spec.match_file(rel_path)

def detect_language(file_path):
    """Detect language from file extension for code block markers."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.py':
        return 'python'
    elif ext == '.js':
        return 'javascript'
    elif ext == '.html':
        return 'html'
    elif ext == '.css':
        return 'css'
    else:
        return ''  # Plain text or unknown

def generate_structure(output_file, base_dir):
    entries = []
    spec = load_gitignore(base_dir)

    # Walk through the directory
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip files matching .gitignore
            if is_ignored(file_path, base_dir, spec):
                continue

            # Calculate relative path from base_dir
            rel_path = os.path.relpath(file_path, base_dir)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

            # Detect language for code block markers
            language = detect_language(file_path)
            if language:
                block = f"'''{language}\n{content.rstrip()}\n'''"
            else:
                block = content.rstrip()

            # Compose the entry
            entry = f"### {rel_path}\n{block}"
            entries.append(entry)

    # Join all entries with two newlines for clarity
    final_content = '\n\n'.join(entries)

    # Write to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Structure written to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Export file structure respecting .gitignore")
    parser.add_argument('base_dir', help="Base directory to scan")
    parser.add_argument('output_file', help="Output file (e.g., application_out.txt)")
    args = parser.parse_args()

    if not os.path.isdir(args.base_dir):
        print(f"Error: Directory {args.base_dir} does not exist")
        return

    generate_structure(args.output_file, args.base_dir)

if __name__ == "__main__":
    main()
