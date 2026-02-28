"""
Snippet Manager — Save, retrieve, and search reusable code snippets.

Usage:
    python -m devtoolkit snippet add <name> [--file FILE] [--lang LANG] [--tag TAG]
    python -m devtoolkit snippet get <name>
    python -m devtoolkit snippet list [--tag TAG]
    python -m devtoolkit snippet search <query>
    python -m devtoolkit snippet remove <name>
    python -m devtoolkit snippet export [--file FILE]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SNIPPETS_FILE = Path.home() / ".devtoolkit_snippets.json"


def load_snippets() -> dict:
    if not SNIPPETS_FILE.exists():
        return {}
    try:
        with open(SNIPPETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_snippets(snippets: dict) -> None:
    with open(SNIPPETS_FILE, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)


def cmd_add(args) -> None:
    snippets = load_snippets()

    if args.file:
        path = Path(args.file)
        if not path.is_file():
            print(f"  Error: File '{args.file}' not found.")
            return
        code = path.read_text(encoding="utf-8")
        lang = args.lang or path.suffix.lstrip(".")
    else:
        print("  Enter snippet code (Ctrl+Z then Enter on Windows, Ctrl+D on Unix to finish):")
        try:
            code = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n  Cancelled.")
            return
        lang = args.lang or "text"

    snippets[args.name] = {
        "code": code,
        "language": lang,
        "tags": args.tag or [],
        "description": args.desc or "",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
    }
    save_snippets(snippets)
    print(f"  Saved snippet '{args.name}' ({len(code)} chars, {lang})")


def cmd_get(args) -> None:
    snippets = load_snippets()
    if args.name not in snippets:
        print(f"  Snippet '{args.name}' not found.")
        # Suggest similar names
        suggestions = [n for n in snippets if args.name.lower() in n.lower()]
        if suggestions:
            print(f"  Did you mean: {', '.join(suggestions)}?")
        return

    s = snippets[args.name]
    if args.raw:
        print(s["code"], end="")
    else:
        print(f"\n  {'─' * 55}")
        print(f"  {args.name}  [{s['language']}]")
        if s.get("description"):
            print(f"  {s['description']}")
        if s.get("tags"):
            print(f"  Tags: {', '.join(s['tags'])}")
        print(f"  {'─' * 55}")
        for line in s["code"].splitlines():
            print(f"  {line}")
        print(f"  {'─' * 55}\n")


def cmd_list(args) -> None:
    snippets = load_snippets()
    if not snippets:
        print("\n  No snippets saved. Add one with: devtoolkit snippet add <name>")
        return

    filtered = snippets
    if args.tag:
        filtered = {n: s for n, s in snippets.items() if args.tag in s.get("tags", [])}

    print(f"\n  {'─' * 60}")
    print(f"  SNIPPETS ({len(filtered)} total)")
    print(f"  {'─' * 60}")
    print(f"  {'Name':<20} {'Lang':<10} {'Tags':<15} {'Size':>8}")
    print(f"  {'─' * 60}")

    for name, s in sorted(filtered.items()):
        lang = s.get("language", "?")
        tags = ", ".join(s.get("tags", [])) or "—"
        size = f"{len(s['code'])} ch"
        print(f"  {name:<20} {lang:<10} {tags:<15} {size:>8}")

    print(f"  {'─' * 60}\n")


def cmd_search(args) -> None:
    snippets = load_snippets()
    query = args.query.lower()
    results = {}
    for name, s in snippets.items():
        if (query in name.lower() or
            query in s.get("code", "").lower() or
            query in s.get("description", "").lower() or
            any(query in t.lower() for t in s.get("tags", []))):
            results[name] = s

    if not results:
        print(f"  No snippets matching '{args.query}'.")
        return

    print(f"\n  Found {len(results)} snippet(s) matching '{args.query}':\n")
    for name, s in results.items():
        lines = s["code"].splitlines()
        preview = lines[0][:60] if lines else "(empty)"
        print(f"    {name} [{s.get('language', '?')}] — {preview}...")


def cmd_remove(args) -> None:
    snippets = load_snippets()
    if args.name in snippets:
        del snippets[args.name]
        save_snippets(snippets)
        print(f"  Removed snippet '{args.name}'.")
    else:
        print(f"  Snippet '{args.name}' not found.")


def cmd_export(args) -> None:
    snippets = load_snippets()
    if not snippets:
        print("  No snippets to export.")
        return

    output = args.file or "snippets_export.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)
    print(f"  Exported {len(snippets)} snippet(s) to {output}")


def cmd_import(args) -> None:
    path = Path(args.file)
    if not path.is_file():
        print(f"  Error: File '{args.file}' not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        imported = json.load(f)

    snippets = load_snippets()
    count = 0
    for name, data in imported.items():
        if name not in snippets or args.overwrite:
            snippets[name] = data
            count += 1

    save_snippets(snippets)
    print(f"  Imported {count} snippet(s) from {args.file}")


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit snippet",
        description="Save, retrieve, and search reusable code snippets.",
    )
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Save a new snippet")
    p_add.add_argument("name", help="Snippet name/key")
    p_add.add_argument("-f", "--file", help="Read snippet from file")
    p_add.add_argument("-l", "--lang", help="Language (auto-detected from file ext)")
    p_add.add_argument("-t", "--tag", action="append", help="Add a tag")
    p_add.add_argument("-d", "--desc", help="Short description")

    # get
    p_get = sub.add_parser("get", help="Retrieve a snippet")
    p_get.add_argument("name", help="Snippet name")
    p_get.add_argument("--raw", action="store_true", help="Output raw code only")

    # list
    p_list = sub.add_parser("list", help="List all snippets")
    p_list.add_argument("-t", "--tag", help="Filter by tag")

    # search
    p_search = sub.add_parser("search", help="Search snippets")
    p_search.add_argument("query", help="Search query")

    # remove
    p_rm = sub.add_parser("remove", help="Delete a snippet")
    p_rm.add_argument("name", help="Snippet name")

    # export
    p_export = sub.add_parser("export", help="Export snippets to JSON")
    p_export.add_argument("-f", "--file", help="Output file (default: snippets_export.json)")

    # import
    p_import = sub.add_parser("import", help="Import snippets from JSON")
    p_import.add_argument("file", help="JSON file to import")
    p_import.add_argument("--overwrite", action="store_true", help="Overwrite existing snippets")

    args = parser.parse_args(argv)

    if not args.command:
        cmd_list(argparse.Namespace(tag=None))
        return 0

    commands = {
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "search": cmd_search,
        "remove": cmd_remove,
        "export": cmd_export,
        "import": cmd_import,
    }
    commands[args.command](args)
    return 0
