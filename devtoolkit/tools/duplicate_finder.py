"""
Duplicate File Finder — Finds duplicate files by content hash.

Usage:
    python -m devtoolkit dupes [DIRECTORY] [--recursive] [--delete] [--min-size SIZE]
"""

import argparse
import hashlib
import os
from collections import defaultdict
from pathlib import Path


def file_hash(filepath: str, chunk_size: int = 8192) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(directory: str, recursive: bool = True, min_size: int = 0) -> dict[str, list[str]]:
    """Return a dict of hash -> [filepaths] for all duplicates."""
    directory = Path(directory).resolve()
    if not directory.is_dir():
        print(f"  Error: '{directory}' is not a valid directory.")
        return {}

    # Phase 1: Group by file size (fast pre-filter)
    size_groups: dict[int, list[Path]] = defaultdict(list)
    pattern = "**/*" if recursive else "*"
    for item in directory.glob(pattern):
        if item.is_file() and item.stat().st_size >= min_size:
            size_groups[item.stat().st_size].append(item)

    # Phase 2: Hash only files that share a size
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for size, files in size_groups.items():
        if len(files) < 2:
            continue
        for f in files:
            try:
                h = file_hash(str(f))
                hash_groups[h].append(str(f))
            except (PermissionError, OSError):
                pass

    # Keep only actual duplicates
    return {h: paths for h, paths in hash_groups.items() if len(paths) > 1}


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit dupes",
        description="Find duplicate files by content hash.",
    )
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to scan (default: current dir)")
    parser.add_argument("-r", "--recursive", action="store_true", default=True,
                        help="Scan subdirectories (default: True)")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive",
                        help="Don't scan subdirectories")
    parser.add_argument("--min-size", type=int, default=1,
                        help="Minimum file size in bytes (default: 1)")
    parser.add_argument("--delete", action="store_true",
                        help="Interactively delete duplicates (keeps first)")
    args = parser.parse_args(argv)

    print(f"\n  Scanning '{Path(args.directory).resolve()}' for duplicates...\n")
    dupes = find_duplicates(args.directory, args.recursive, args.min_size)

    if not dupes:
        print("  No duplicate files found.")
        return 0

    total_waste = 0
    group_num = 0
    for hash_val, paths in dupes.items():
        group_num += 1
        size = os.path.getsize(paths[0])
        waste = size * (len(paths) - 1)
        total_waste += waste

        print(f"  Group {group_num} ({format_size(size)} each, {len(paths)} copies):")
        for i, p in enumerate(paths):
            marker = " [KEEP]" if i == 0 else ""
            print(f"    {'>' if i == 0 else ' '} {p}{marker}")

        if args.delete:
            answer = input(f"\n  Delete {len(paths)-1} duplicate(s) from group {group_num}? [y/N] ").strip().lower()
            if answer == "y":
                for p in paths[1:]:
                    os.remove(p)
                    print(f"    Deleted: {p}")
        print()

    print(f"  Summary: {group_num} group(s) of duplicates found.")
    print(f"  Wasted space: {format_size(total_waste)}")
    return 0
