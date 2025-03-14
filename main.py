#!/usr/bin/env python3

import shutil
import os
import difflib
import argparse

def witch(command: str):
    # Try finding the command normally
    path = shutil.which(command)
    if path:
        print(path)
        return path

    # If not found, try fuzzy matching against executables in PATH
    paths = os.environ["PATH"].split(os.pathsep)
    executables = {f for p in paths if os.path.isdir(p) for f in os.listdir(p)}

    matches = difflib.get_close_matches(command, executables, n=5, cutoff=0.4)
    if matches:
        print("Command not found. Did you mean:")
        for match in matches:
            match_path = shutil.which(match)  # Get full path of each match
            if match_path:
                print(f"  - {match} ({match_path})")
            else:
                print(f"  - {match} (not found in PATH)")
    else:
        print("Command not found and no close matches.")

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A smarter 'which' command with fuzzy matching.")
    parser.add_argument("command", help="The command to search for.")
    args = parser.parse_args()

    witch(args.command)
