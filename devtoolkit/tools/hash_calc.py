"""
Hash Calculator — Compute MD5, SHA1, SHA256 hashes for files and text.

Usage:
    python -m devtoolkit hash <file_or_text> [--algo ALGO] [--compare HASH] [--all]
"""

import argparse
import hashlib
from pathlib import Path


ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]


def hash_bytes(data: bytes, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(data)
    return h.hexdigest()


def hash_file(filepath: str, algo: str, chunk_size: int = 8192) -> str:
    h = hashlib.new(algo)
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit hash",
        description="Compute hashes for files and text strings.",
    )
    parser.add_argument("input", help="File path or text string to hash")
    parser.add_argument("-a", "--algo", default="sha256",
                        choices=ALGORITHMS, help="Hash algorithm (default: sha256)")
    parser.add_argument("--all", action="store_true",
                        help="Show all algorithms at once")
    parser.add_argument("-c", "--compare",
                        help="Compare result against this hash value")
    parser.add_argument("-t", "--text", action="store_true",
                        help="Force treating input as text (not a file)")
    args = parser.parse_args(argv)

    path = Path(args.input)
    is_file = path.is_file() and not args.text

    print()
    if is_file:
        size = path.stat().st_size
        print(f"  File:  {path.resolve()}")
        print(f"  Size:  {format_size(size)} ({size:,} bytes)")
    else:
        print(f"  Text:  \"{args.input}\"")
        print(f"  Size:  {len(args.input.encode('utf-8'))} bytes (UTF-8)")

    print(f"  {'─' * 55}")

    algos = ALGORITHMS if args.all else [args.algo]
    results = {}

    for algo in algos:
        if is_file:
            digest = hash_file(str(path), algo)
        else:
            digest = hash_bytes(args.input.encode("utf-8"), algo)
        results[algo] = digest
        print(f"  {algo.upper():<8}  {digest}")

    if args.compare:
        compare_lower = args.compare.lower().strip()
        matched = any(v == compare_lower for v in results.values())
        print(f"\n  Compare: {args.compare}")
        if matched:
            print(f"  Result:  MATCH ✓")
        else:
            print(f"  Result:  NO MATCH ✗")

    print()
    return 0
