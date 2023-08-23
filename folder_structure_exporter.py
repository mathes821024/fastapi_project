"""
Folder Structure Exporter (folder_structure_exporter.py)

Description:
    This script traverses a given directory and exports its structure,
    along with the content of selected files, to a text file. It's especially useful
    for documenting the content and structure of projects.

Author:
    [Your Name or Alias]

Date:
    [Creation Date, e.g., 2023-08-23]

Usage:
    python folder_structure_exporter.py [FOLDER_PATH] [LINES]

    Arguments:
    - FOLDER_PATH: The path to the directory you want to traverse. (Mandatory)
    - LINES: The number of lines of content you want to capture from each file.
             If not provided, the script will capture all lines. (Optional)

Examples:
    1. To traverse the 'my_project' directory and capture all lines of content:
       python folder_structure_exporter.py ./my_project

    2. To traverse the 'my_project' directory and capture only the first 5 lines of content:
       python folder_structure_exporter.py ./my_project 5

Dependencies:
    - chardet: Used to detect the encoding of the files before reading.

Note:
    This script is designed to be cross-platform and should work on both Windows and Linux.
    The selected files for content capture are: .h, .c, .py, .go, and makefile.
"""

# [The rest of your code...]
# Optimized script for exporting folder structure and content

import os
import datetime
import codecs
import chardet
import argparse

EXCLUDED_DIRS = ['.git', '.idea']
INCLUDED_FILE_EXTENSIONS = ['.py', '.c', '.ini', '.cpp', 'Makefile', '.go']

def write_file_structure_and_content_to_txt(folder_path, lines, depth=0):
    # Form the output filename
    now = datetime.datetime.now().strftime("%Y%m%d")
    output_file = f"output_{os.path.basename(folder_path)}_{now}.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        _write_folder_content(f, folder_path, lines, depth)

def _write_folder_content(f, folder_path, lines, depth):
    items = sorted(os.listdir(folder_path))
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and item not in EXCLUDED_DIRS:
            f.write('\t' * depth + f'Directory: {item}\n')
            _write_folder_content(f, item_path, lines, depth + 1)
        elif any(item.endswith(ext) for ext in INCLUDED_FILE_EXTENSIONS):
            f.write('\t' * depth + f'File: {item}\n')
            with _open_with_detected_encoding(item_path) as content_file:
                if content_file:
                    f.write('\t' * depth + 'Content:\n')
                    for i, line in enumerate(content_file):
                        if lines != -1 and i >= lines:
                            f.write('\t' * depth + '...\n')
                            break
                        f.write('\t' * depth + line)
                else:
                    f.write('\t' * depth + 'Empty File\n')

def _open_with_detected_encoding(filepath):
    try:
        rawdata = open(filepath, 'rb').read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        return codecs.open(filepath, 'r', encoding)
    except Exception as e:
        print(f"Error opening file with detected encoding: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Write file structure and content to txt")
    parser.add_argument("folder_path", help="Path of the folder to process")
    parser.add_argument("--lines", type=int, default=-1, help="Number of lines to write for each file. Default is all lines.")
    args = parser.parse_args()
    write_file_structure_and_content_to_txt(args.folder_path, args.lines)

if __name__ == '__main__':
    main()

# 在windows下展示目录结构
# (dir /s /b *.py *.c *.ini *.cpp Makefile *.go) > files.txt

# 在linux下展示目录结构
# find . -type f \( -iname "*.py" -o -iname "*.c" -o -iname "*.ini" -o -iname "*.cpp" -o -iname "Makefile" -o -iname "*.go" \) > files.txt

