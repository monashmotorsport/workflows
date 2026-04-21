"""
Verify Git Committer
--------------------

Checks that the git commit is being made by someone with a valid email address, and a
mathching name.

Usage
-----
>>> python verify-committer.py --domain monashmotorsport.com --check-name
"""

import re
import argparse
import subprocess

from typing import Tuple


def get_git_user_info() -> Tuple[str, str]:
    """Get the git user name and email from the local git config."""
    name = subprocess.check_output(["git", "config", "user.name"]).decode().strip()
    email = subprocess.check_output(["git", "config", "user.email"]).decode().strip()
    return name, email


def is_valid_email(email: str, domain: str) -> bool:
    """Check if the email is valid and belongs to the specified domain."""
    pattern = rf"^[\w\.-]+@{re.escape(domain)}$"
    return re.match(pattern, email) is not None


def is_matching_name(name: str, email: str) -> bool:
    """Check if the name matches the email (e.g. John Doe <john.doe@domain.com>)."""
    email_name = email.split("@")[0]

    name_parts = re.split(r"[\s\._-]+", name.lower())
    email_parts = re.split(r"[\s\._-]+", email_name.lower())

    return all(part in name_parts for part in email_parts)


def main():
    parser = argparse.ArgumentParser(description="Verify Git committer information.")
    parser.add_argument(
        "--domain",
        required=True,
        help="The email domain to check against (e.g. monashmotorsport.com).",
    )
    parser.add_argument(
        "--check-name",
        action="store_true",
        help="Also check that the name matches the email.",
    )
    args = parser.parse_args()

    name, email = get_git_user_info()

    if email == "" and name == "":
        # Skip checks if running from CI without git user configured
        return 0

    exit_code = 0

    if not is_valid_email(email, args.domain):
        print(
            f"Error: Email '{email}' is not valid or does not belong to"
            f"'{args.domain}'."
        )
        exit_code = 1

    if args.check_name and not is_matching_name(name, email):
        print(f"Error: Name '{name}' does not match email '{email}'.")
        exit_code = 1

    if exit_code != 0:
        print("Please configure your git user.name and user.email correctly.")
        print("Example: git config --global user.name 'John Doe'")
        print(f"         git config --global user.email 'john.doe@{args.domain}'")

    return exit_code


if __name__ == "__main__":
    exit(main())
