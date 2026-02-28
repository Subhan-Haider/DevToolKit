r"""
Regex Tester — Test regex patterns interactively against text or files.

Usage:
    python -m devtoolkit regex <PATTERN> [TEXT_OR_FILE] [--multiline] [--global]
    python -m devtoolkit regex "(\d{3})-(\d{4})" "Call 555-1234 or 555-5678" --global
"""

import argparse
import re
from pathlib import Path


# Common useful regex patterns as a quick reference
CHEATSHEET = {
    "email":    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url":      r"https?://[^\s<>\"']+",
    "ipv4":     r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "phone":    r"\+?[\d\s\-().]{7,15}",
    "date":     r"\d{4}-\d{2}-\d{2}",
    "hex":      r"#?[0-9a-fA-F]{6}\b",
    "uuid":     r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "semver":   r"\bv?\d+\.\d+\.\d+(?:-[\w.]+)?(?:\+[\w.]+)?\b",
}


def explain_pattern(pattern: str) -> list[str]:
    """Provide a basic explanation of regex components."""
    explanations = {
        r"\d": "digit [0-9]",
        r"\w": "word char [a-zA-Z0-9_]",
        r"\s": "whitespace",
        r"\b": "word boundary",
        r".": "any character",
        r"*": "0 or more (greedy)",
        r"+": "1 or more (greedy)",
        r"?": "0 or 1 (optional)",
        r"*?": "0 or more (lazy)",
        r"+?": "1 or more (lazy)",
        r"^": "start of string/line",
        r"$": "end of string/line",
        r"\n": "newline",
        r"\t": "tab",
    }
    notes = []
    for token, desc in explanations.items():
        if token in pattern:
            notes.append(f"    {token:<6} → {desc}")

    # Detect groups
    groups = re.findall(r"\((?:\?P<(\w+)>)?", pattern)
    if groups:
        for i, g in enumerate(groups, 1):
            if g:
                notes.append(f"    Group {i}: named '{g}'")
            else:
                notes.append(f"    Group {i}: capturing group")
    return notes


def highlight_matches(text: str, matches: list[re.Match]) -> str:
    """Create a visual representation of matches in text."""
    if not matches:
        return text

    result = []
    last_end = 0
    for m in matches:
        result.append(text[last_end:m.start()])
        result.append(f">>>{m.group()}<<<")
        last_end = m.end()
    result.append(text[last_end:])
    return "".join(result)


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit regex",
        description="Test regex patterns against text or files.",
    )
    parser.add_argument("pattern", nargs="?",
                        help="Regex pattern to test (or a preset name like 'email')")
    parser.add_argument("text", nargs="?",
                        help="Text to test against (or file path)")
    parser.add_argument("-g", "--global", action="store_true", dest="find_all",
                        help="Find all matches (not just first)")
    parser.add_argument("-m", "--multiline", action="store_true",
                        help="Enable multiline mode (^ and $ match line boundaries)")
    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help="Case-insensitive matching")
    parser.add_argument("--cheatsheet", action="store_true",
                        help="Show common regex patterns")
    parser.add_argument("-e", "--explain", action="store_true",
                        help="Explain the regex pattern components")
    args = parser.parse_args(argv)

    print()

    if args.cheatsheet:
        print(f"  Regex Cheatsheet — Common Patterns")
        print(f"  {'─' * 55}")
        for name, pat in CHEATSHEET.items():
            print(f"    {name:<10}  {pat}")
        print(f"\n  Use these as patterns: devtoolkit regex email \"test@example.com\"")
        print()
        return 0

    if not args.pattern:
        parser.print_help()
        return 0

    # Resolve preset patterns
    pattern_str = CHEATSHEET.get(args.pattern, args.pattern)
    if args.pattern in CHEATSHEET:
        print(f"  Using preset '{args.pattern}': {pattern_str}")

    # Compile
    flags = 0
    if args.multiline:
        flags |= re.MULTILINE
    if args.ignore_case:
        flags |= re.IGNORECASE

    try:
        compiled = re.compile(pattern_str, flags)
    except re.error as e:
        print(f"  Regex Error: {e}")
        return 1

    print(f"  Pattern:  /{pattern_str}/{'i' if args.ignore_case else ''}{'m' if args.multiline else ''}{'g' if args.find_all else ''}")

    if args.explain:
        notes = explain_pattern(pattern_str)
        if notes:
            print(f"  {'─' * 55}")
            print(f"  Pattern breakdown:")
            for n in notes:
                print(n)

    if not args.text:
        if args.explain:
            print()
            return 0
        # Interactive mode
        print(f"  {'─' * 55}")
        print(f"  Enter text to test (empty line to quit):\n")
        while True:
            try:
                text = input("  > ")
            except (EOFError, KeyboardInterrupt):
                break
            if not text:
                break
            matches = list(compiled.finditer(text))
            if matches:
                print(f"    ✓ {len(matches)} match(es): {highlight_matches(text, matches)}")
                for m in matches:
                    if m.groups():
                        print(f"      Groups: {m.groups()}")
            else:
                print(f"    ✗ No match")
        print()
        return 0

    # Check if it's a file
    text = args.text
    path = Path(args.text)
    if path.is_file():
        try:
            text = path.read_text(encoding="utf-8")
            print(f"  File:     {path.resolve()}")
        except Exception as e:
            print(f"  Error reading file: {e}")
            return 1

    print(f"  {'─' * 55}")

    if args.find_all:
        matches = list(compiled.finditer(text))
        if matches:
            print(f"  Found {len(matches)} match(es):\n")
            for i, m in enumerate(matches, 1):
                print(f"    {i}. \"{m.group()}\"  (pos {m.start()}-{m.end()})")
                if m.groups():
                    for gi, g in enumerate(m.groups(), 1):
                        print(f"       Group {gi}: \"{g}\"")
        else:
            print(f"  No matches found.")
    else:
        m = compiled.search(text)
        if m:
            print(f"  Match:    \"{m.group()}\"  (pos {m.start()}-{m.end()})")
            if m.groups():
                for gi, g in enumerate(m.groups(), 1):
                    print(f"  Group {gi}:  \"{g}\"")
            print(f"\n  Highlighted: {highlight_matches(text[:200], [m])}")
        else:
            print(f"  No match found.")

    print()
    return 0
