#!/usr/bin/env python3
"""
A smarter 'which' command with fuzzy matching.

This script attempts to locate an executable in the system PATH.
If the exact command is not found, it uses fuzzy matching to suggest
commands that closely resemble the input.

Usage:
    python witch.py <command>
"""

import os
import re
import shutil
import difflib
import argparse
from typing import Optional

from wcwidth import wcswidth

# ANSI color codes for terminal output.
ANSI_GREEN: str = "\033[92m"
ANSI_RED: str = "\033[91m"
ANSI_MAGENTA: str = "\033[95m"
ANSI_RESET: str = "\033[0m"

# Regex pattern to remove ANSI escape codes.
ANSI_ESCAPE_RE: re.Pattern = re.compile(r'\033\[[0-9;]*m')

def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape codes from a given text.

    Args:
        text (str): The text that may include ANSI escape sequences.

    Returns:
        str: The text with ANSI escape codes removed.
    """
    return ANSI_ESCAPE_RE.sub('', text)

def highlight_differences(input_word: str, suggestion: str) -> str:
    """
    Highlight the differences between the input word and the suggested command.

    Correctly matching letters are highlighted in green, replaced letters in red,
    and inserted letters in magenta.

    Args:
        input_word (str): The original command input by the user.
        suggestion (str): The suggested command to compare against.

    Returns:
        str: The suggestion with ANSI color codes applied to differing parts.
    """
    matcher: difflib.SequenceMatcher = difflib.SequenceMatcher(None, input_word, suggestion)
    highlighted: str = ""

    for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            highlighted += f"{ANSI_GREEN}{suggestion[j1:j2]}{ANSI_RESET}"
        elif tag == "replace":
            highlighted += f"{ANSI_RED}{suggestion[j1:j2]}{ANSI_RESET}"
        elif tag == "insert":
            highlighted += f"{ANSI_MAGENTA}{suggestion[j1:j2]}{ANSI_RESET}"

    return highlighted

def pad_string(text: str, width: int) -> str:
    """
    Pad a string with spaces so that its visible width matches the given width.

    ANSI escape codes are not counted toward the visible width.

    Args:
        text (str): The string to pad.
        width (int): The desired visible width.

    Returns:
        str: The padded string.
    """
    visible_width: int = wcswidth(strip_ansi(text))
    return text + " " * (width - visible_width)

def witch(command: str) -> Optional[str]:
    """
    Locate an executable in the system PATH or suggest close matches.

    The function first attempts to find the command using a direct lookup.
    If not found, it uses fuzzy matching against executables available in the PATH,
    printing suggestions with highlighted differences.

    Args:
        command (str): The command to search for.

    Returns:
        Optional[str]: The path to the command if found; otherwise, None.
    """
    # Try to locate the command normally.
    path: Optional[str] = shutil.which(command)
    if path:
        print(path)
        return path

    # If the command is not found, attempt fuzzy matching.
    paths = os.environ.get("PATH", "").split(os.pathsep)
    executables = {f for p in paths if os.path.isdir(p) for f in os.listdir(p)}

    matches = difflib.get_close_matches(command, executables, n=5, cutoff=0.4)
    if matches:
        print("\nCommand not found. Did you mean:\n")

        # Define column widths.
        cmd_width: int = 20
        path_width: int = 50

        # Print header.
        print(f"{pad_string('Suggested Command', cmd_width)} | {pad_string('Location', path_width)}")
        print("-" * (cmd_width + path_width + 3))

        for match in matches:
            highlighted_match: str = highlight_differences(command, match)
            match_path: Optional[str] = shutil.which(match) or "(not found in PATH)"
            print(f"{pad_string(highlighted_match, cmd_width)} | {pad_string(match_path, path_width)}")
    else:
        print("Command not found and no close matches.")

    return None

def main() -> None:
    """
    Parse command-line arguments and execute the command lookup.

    This function serves as the entry point for the script.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="A smarter 'which' command with fuzzy matching."
    )
    parser.add_argument("command", help="The command to search for.")
    args: argparse.Namespace = parser.parse_args()
    witch(args.command)

if __name__ == "__main__":
    main()
