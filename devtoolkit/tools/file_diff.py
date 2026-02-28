"""
File Diff — Compare two files and show differences.

Usage:
    python -m devtoolkit diff <file1> <file2> [--context N] [--side-by-side] [--html]
"""

import argparse
import difflib
from pathlib import Path


def colorize_diff(lines: list[str]) -> list[str]:
    """Add visual markers to diff lines."""
    result = []
    for line in lines:
        if line.startswith("+++") or line.startswith("---"):
            result.append(f"  {line}")
        elif line.startswith("@@"):
            result.append(f"  {line}")
        elif line.startswith("+"):
            result.append(f"  + {line[1:]}")
        elif line.startswith("-"):
            result.append(f"  - {line[1:]}")
        else:
            result.append(f"    {line}")
    return result


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit diff",
        description="Compare two files and show differences.",
    )
    parser.add_argument("file1", help="First file")
    parser.add_argument("file2", help="Second file")
    parser.add_argument("-c", "--context", type=int, default=3,
                        help="Lines of context around changes (default: 3)")
    parser.add_argument("-s", "--side-by-side", action="store_true",
                        help="Side-by-side comparison")
    parser.add_argument("--html", action="store_true",
                        help="Generate an HTML diff report")
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics only")
    args = parser.parse_args(argv)

    path1, path2 = Path(args.file1), Path(args.file2)

    if not path1.is_file():
        print(f"  Error: '{args.file1}' not found.")
        return 1
    if not path2.is_file():
        print(f"  Error: '{args.file2}' not found.")
        return 1

    try:
        lines1 = path1.read_text(encoding="utf-8").splitlines(keepends=True)
        lines2 = path2.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        print("  Error: One or both files appear to be binary.")
        return 1

    # Calculate stats
    added = 0
    removed = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, lines1, lines2).get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            added += j2 - j1
            removed += i2 - i1

    ratio = difflib.SequenceMatcher(None, lines1, lines2).ratio()

    print(f"\n  Comparing:")
    print(f"    A: {path1.resolve()} ({len(lines1)} lines)")
    print(f"    B: {path2.resolve()} ({len(lines2)} lines)")
    print(f"  {'─' * 55}")
    print(f"  +{added} added, -{removed} removed | {ratio:.1%} similar")

    if args.stats:
        print()
        return 0

    if lines1 == lines2:
        print(f"\n  Files are identical.\n")
        return 0

    if args.html:
        differ = difflib.HtmlDiff(wrapcolumn=80)
        html_content = differ.make_file(
            lines1, lines2,
            fromdesc=str(path1.name),
            todesc=str(path2.name),
            context=True,
            numlines=args.context,
        )
        output_path = Path(f"diff_{path1.stem}_vs_{path2.stem}.html")
        output_path.write_text(html_content, encoding="utf-8")
        print(f"\n  HTML diff saved to: {output_path.resolve()}")
        print()
        return 0

    if args.side_by_side:
        width = 40
        print(f"\n  {'A':<{width}} | {'B':<{width}}")
        print(f"  {'─' * width}-+-{'─' * width}")

        differ = difflib.ndiff(
            [l.rstrip() for l in lines1],
            [l.rstrip() for l in lines2]
        )
        for line in differ:
            code = line[:2]
            text = line[2:]
            if code == "- ":
                print(f"  {text:<{width}} | {'':>{width}}")
            elif code == "+ ":
                print(f"  {'':>{width}} | {text:<{width}}")
            elif code == "  ":
                print(f"  {text:<{width}} | {text:<{width}}")
    else:
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=str(path1),
            tofile=str(path2),
            n=args.context,
        )
        diff_lines = list(diff)
        if diff_lines:
            print()
            formatted = colorize_diff([l.rstrip() for l in diff_lines])
            for line in formatted:
                print(line)
        else:
            print(f"\n  No differences found.")

    print()
    return 0
