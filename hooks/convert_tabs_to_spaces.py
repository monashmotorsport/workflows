"""
Convert tabs to spaces
======================

Convert tabs to spaces in a file or set of files.

Usage
-----
>>> python convert-tabs-to-spaces.py path/to/file --spaces 4
"""

import argparse


def convert_tabs_to_spaces(file_path: str, spaces: int = 4) -> None:
    """Convert tabs to spaces in the specified file."""
    with open(file_path, "r") as f:
        content = f.read()

    new_content = content.replace("\t", " " * spaces)

    with open(file_path, "w") as f:
        f.write(new_content)


def main():
    parser = argparse.ArgumentParser(description="Convert tabs to spaces in a file.")
    parser.add_argument("paths", nargs="+", help="Path(s) to the file(s) to convert")
    parser.add_argument(
        "--spaces",
        type=int,
        default=4,
        help="Number of spaces to replace each tab with (default: 4).",
    )
    args = parser.parse_args()

    for path in args.paths:
        convert_tabs_to_spaces(path, args.spaces)


if __name__ == "__main__":
    main()
