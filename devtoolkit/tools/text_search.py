"""
Text Search — Search for text/regex patterns in files recursively.

Usage:
    python -m devtoolkit search <PATTERN> [DIRECTORY] [--ext EXT] [--ignore-case]
                                [--regex] [--context N] [--count-only]
"""

import argparse
import os
import re
from pathlib import Path


# File extensions to skip (binary files)
BINARY_EXTENSIONS = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".obj", ".o",
    ".pyc", ".pyd", ".class", ".jar",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".mp3", ".mp4", ".avi", ".mkv", ".mov", ".wav", ".flac",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".ttf", ".otf", ".woff", ".woff2",
    ".sqlite", ".db",
}

# Directories to always skip
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", "dist", "build",
    ".eggs", "*.egg-info",
}


def is_binary(filepath: Path) -> bool:
    """Quick check if file is likely binary."""
    if filepath.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except (PermissionError, OSError):
        return True


def search_file(filepath: Path, pattern, context_lines: int = 0) -> list[dict]:
    """Search a single file for the pattern. Returns list of matches."""
    matches = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (PermissionError, OSError):
        return []

    for i, line in enumerate(lines, 1):
        if pattern.search(line):
            match_info = {
                "line_num": i,
                "line": line.rstrip("\n\r"),
                "context_before": [],
                "context_after": [],
            }
            if context_lines > 0:
                start = max(0, i - 1 - context_lines)
                end = min(len(lines), i + context_lines)
                match_info["context_before"] = [
                    (start + j + 1, lines[start + j].rstrip("\n\r"))
                    for j in range(i - 1 - start)
                ]
                match_info["context_after"] = [
                    (i + j + 1, lines[i + j].rstrip("\n\r"))
                    for j in range(end - i)
                ]
            matches.append(match_info)

    return matches


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit search",
        description="Search for text/regex patterns in files.",
    )
    parser.add_argument("pattern", help="Search pattern (text or regex)")
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to search (default: current dir)")
    parser.add_argument("-e", "--ext", action="append",
                        help="File extensions to include (e.g., -e .py -e .js)")
    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help="Case-insensitive search")
    parser.add_argument("-r", "--regex", action="store_true",
                        help="Treat pattern as a regular expression")
    parser.add_argument("-C", "--context", type=int, default=0,
                        help="Lines of context around matches")
    parser.add_argument("--count-only", action="store_true",
                        help="Only show match counts per file")
    parser.add_argument("--max-results", type=int, default=500,
                        help="Maximum number of matches to show (default: 500)")
    args = parser.parse_args(argv)

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        print(f"  Error: '{directory}' is not a valid directory.")
        return 1

    # Compile pattern
    flags = re.IGNORECASE if args.ignore_case else 0
    try:
        if args.regex:
            compiled = re.compile(args.pattern, flags)
        else:
            compiled = re.compile(re.escape(args.pattern), flags)
    except re.error as e:
        print(f"  Error in regex pattern: {e}")
        return 1

    print(f"\n  Searching for '{args.pattern}' in {directory}...\n")

    total_matches = 0
    total_files = 0
    files_with_matches = 0

    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in sorted(files):
            filepath = Path(root) / filename

            # Filter by extension if specified
            if args.ext:
                if filepath.suffix.lower() not in [e if e.startswith(".") else f".{e}" for e in args.ext]:
                    continue

            if is_binary(filepath):
                continue

            total_files += 1
            matches = search_file(filepath, compiled, args.context)

            if not matches:
                continue

            files_with_matches += 1
            rel_path = filepath.relative_to(directory)

            if args.count_only:
                print(f"  {rel_path}: {len(matches)} match(es)")
                total_matches += len(matches)
                continue

            print(f"  {rel_path}")
            for m in matches:
                if total_matches >= args.max_results:
                    print(f"\n  ... truncated at {args.max_results} results. Use --max-results to increase.")
                    break

                # Context before
                for num, text in m["context_before"]:
                    print(f"    {num:>5} | {text}")

                # The matching line (highlighted)
                print(f"    {m['line_num']:>5} > {m['line']}")

                # Context after
                for num, text in m["context_after"]:
                    print(f"    {num:>5} | {text}")

                if m["context_before"] or m["context_after"]:
                    print(f"    {'':>5}   ---")

                total_matches += 1

            if total_matches >= args.max_results:
                break
            print()

        if total_matches >= args.max_results:
            break

    print(f"\n  Results: {total_matches} match(es) in {files_with_matches} file(s) ({total_files} files scanned)")
    return 0
