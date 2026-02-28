"""
File Organizer — Automatically sorts files in a directory into
sub-folders by their file extension / category.

Usage:
    python -m devtoolkit organize [DIRECTORY] [--dry-run] [--undo]
"""

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

CATEGORY_MAP = {
    "Images":      {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "Documents":   {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".txt", ".rtf", ".md"},
    "Videos":      {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio":       {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives":    {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Code":        {".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".rb", ".php", ".html", ".css", ".scss", ".json", ".xml", ".yaml", ".yml", ".toml", ".sh", ".bat", ".ps1"},
    "Executables": {".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"},
    "Fonts":       {".ttf", ".otf", ".woff", ".woff2"},
    "Data":        {".csv", ".sql", ".db", ".sqlite", ".parquet"},
}

EXTENSION_TO_CATEGORY = {}
for cat, exts in CATEGORY_MAP.items():
    for ext in exts:
        EXTENSION_TO_CATEGORY[ext] = cat


def categorize(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return EXTENSION_TO_CATEGORY.get(ext, "Other")


def organize(directory: str, dry_run: bool = False) -> list[dict]:
    """Organize files; returns a log of moves."""
    directory = Path(directory).resolve()
    if not directory.is_dir():
        print(f"  Error: '{directory}' is not a valid directory.")
        return []

    moves = []
    for item in directory.iterdir():
        if item.is_dir():
            continue
        if item.name.startswith(".") or item.name == "_organize_log.json":
            continue

        category = categorize(item.name)
        dest_dir = directory / category
        dest_path = dest_dir / item.name

        # Handle name collisions
        counter = 1
        while dest_path.exists():
            stem = item.stem
            dest_path = dest_dir / f"{stem}_{counter}{item.suffix}"
            counter += 1

        move_record = {"src": str(item), "dest": str(dest_path)}
        moves.append(move_record)

        if dry_run:
            print(f"  [DRY RUN] {item.name}  ->  {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            print(f"  Moved: {item.name}  ->  {category}/")

    if not dry_run and moves:
        log_path = directory / "_organize_log.json"
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "moves": moves,
        }
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
        print(f"\n  Log saved to {log_path}  (use --undo to revert)")

    if not moves:
        print("  No files to organize.")
    else:
        print(f"\n  Total: {len(moves)} file(s) {'would be ' if dry_run else ''}organized.")
    return moves


def undo(directory: str) -> None:
    """Revert the last organize operation using the log file."""
    directory = Path(directory).resolve()
    log_path = directory / "_organize_log.json"

    if not log_path.exists():
        print("  No organize log found. Nothing to undo.")
        return

    with open(log_path) as f:
        log_data = json.load(f)

    for record in reversed(log_data["moves"]):
        dest = Path(record["dest"])
        src = Path(record["src"])
        if dest.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(src))
            print(f"  Restored: {dest.name}  ->  {src.parent.name}/")

    # Clean up empty category dirs
    for cat_dir in directory.iterdir():
        if cat_dir.is_dir() and not any(cat_dir.iterdir()):
            cat_dir.rmdir()

    log_path.unlink()
    print(f"\n  Undo complete. {len(log_data['moves'])} file(s) restored.")


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit organize",
        description="Organize files in a directory by type/extension.",
    )
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to organize (default: current dir)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without moving files")
    parser.add_argument("--undo", action="store_true",
                        help="Revert the last organize operation")
    args = parser.parse_args(argv)

    if args.undo:
        undo(args.directory)
    else:
        organize(args.directory, dry_run=args.dry_run)
    return 0
