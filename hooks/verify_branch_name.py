"""
Verify Branch Name
------------------

This pre-commit hook checks that the current Git branch name follows the
category/description format and that the category is one of the allowed types.
Prints an error message indicating why the branch was rejected
- must be in the format category/description
- lowercase, letters and dashes only

Usage
-----
>>> python verify_branch_name.py --categories feature bugfix hotfix release
"""

SPECIAL = ["main", "master"]

CATEGORIES = [
    "feature",
    "bugfix",
    "refactor",
    "test",
    "dev",
    "hotfix",
    "config",
]

import re
import argparse
import subprocess

from verify_commit_author import get_git_user_info


def get_current_branch() -> str:
    """Get the current Git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def validate_branch_name(branch_name: str, categories: list) -> bool:
    """Check if the branch name follows the category/description format."""
    if branch_name in SPECIAL:
        return True

    folders = branch_name.split("/")
    if len(folders) < 2:
        print("INVALID: Branch name must be in the format category/description")
        return False

    if (category := folders[0]) not in categories:
        print(f"INVALID: Branch category '{category}' is not one of the allowed types")
        print(f"Allowed categories: {', '.join(categories)}")
        return False

    for folder in folders:
        if not re.match(r"^[a-z0-9-]+$", folder):
            print(
                f"INVALID: Branch name '{branch_name}' contains invalid characters. "
                "Only lowercase letters, numbers, and dashes are allowed."
            )
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Verify Git branch name format.")
    parser.add_argument(
        "--categories",
        nargs="+",
        default=CATEGORIES,
        help="List of allowed branch categories (default: feature bugfix refactor test "
        "dev hotfix config)",
    )
    parser.add_argument(
        "--special",
        nargs="+",
        default=SPECIAL,
        help="List of special branch names that are always allowed (default: main "
        "master)",
    )
    args = parser.parse_args()

    name, email = get_git_user_info()

    if email == "" and name == "":
        # Skip checks if running from CI without git user configured
        return 0

    branch_name = get_current_branch()
    if validate_branch_name(branch_name, args.categories):
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
