"""
Todo Manager — A persistent, terminal-based todo list.

Usage:
    python -m devtoolkit todo add "Buy groceries"
    python -m devtoolkit todo add "Urgent task" --priority high
    python -m devtoolkit todo list
    python -m devtoolkit todo done 1
    python -m devtoolkit todo remove 1
    python -m devtoolkit todo clear --done
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

TODO_FILE = Path.home() / ".devtoolkit_todos.json"

PRIORITY_SYMBOLS = {"high": "!!!", "medium": "!!", "low": "!", "none": " "}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2, "none": 3}


def load_todos() -> list[dict]:
    """Load todos from file."""
    if not TODO_FILE.exists():
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_todos(todos: list[dict]) -> None:
    """Save todos to file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def next_id(todos: list[dict]) -> int:
    """Get the next available ID."""
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1


def cmd_add(args) -> None:
    """Add a new todo."""
    todos = load_todos()
    todo = {
        "id": next_id(todos),
        "text": args.text,
        "done": False,
        "priority": args.priority,
        "created": datetime.now().isoformat(),
        "completed": None,
        "tags": args.tag or [],
    }
    todos.append(todo)
    save_todos(todos)
    print(f"  Added todo #{todo['id']}: {todo['text']}")


def cmd_list(args) -> None:
    """List all todos."""
    todos = load_todos()
    if not todos:
        print("\n  No todos yet! Add one with: devtoolkit todo add \"Your task\"")
        return

    # Filtering
    if args.tag:
        todos = [t for t in todos if args.tag in t.get("tags", [])]

    if not args.all:
        active = [t for t in todos if not t["done"]]
        done = [t for t in todos if t["done"]]
    else:
        active = [t for t in todos if not t["done"]]
        done = [t for t in todos if t["done"]]

    # Sort by priority
    active.sort(key=lambda t: PRIORITY_ORDER.get(t.get("priority", "none"), 3))

    print(f"\n  {'─' * 60}")
    print(f"  TODO LIST ({len(active)} active, {len(done)} done)")
    print(f"  {'─' * 60}")

    if active:
        for t in active:
            pri = PRIORITY_SYMBOLS.get(t.get("priority", "none"), " ")
            tags = ""
            if t.get("tags"):
                tags = " " + " ".join(f"[{tag}]" for tag in t["tags"])
            print(f"  [ ] #{t['id']:<4} {pri:<3} {t['text']}{tags}")

    if args.all and done:
        print(f"  {'─' * 60}")
        for t in done:
            completed = ""
            if t.get("completed"):
                dt = datetime.fromisoformat(t["completed"])
                completed = f" (done {dt.strftime('%b %d')})"
            print(f"  [x] #{t['id']:<4}     {t['text']}{completed}")

    print(f"  {'─' * 60}\n")


def cmd_done(args) -> None:
    """Mark a todo as done."""
    todos = load_todos()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            t["completed"] = datetime.now().isoformat()
            save_todos(todos)
            print(f"  Completed: #{t['id']} - {t['text']}")
            return
    print(f"  Todo #{args.id} not found.")


def cmd_undone(args) -> None:
    """Mark a todo as not done."""
    todos = load_todos()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = False
            t["completed"] = None
            save_todos(todos)
            print(f"  Reopened: #{t['id']} - {t['text']}")
            return
    print(f"  Todo #{args.id} not found.")


def cmd_remove(args) -> None:
    """Remove a todo."""
    todos = load_todos()
    original_len = len(todos)
    todos = [t for t in todos if t["id"] != args.id]
    if len(todos) < original_len:
        save_todos(todos)
        print(f"  Removed todo #{args.id}.")
    else:
        print(f"  Todo #{args.id} not found.")


def cmd_clear(args) -> None:
    """Clear todos."""
    todos = load_todos()
    if args.done:
        remaining = [t for t in todos if not t["done"]]
        removed = len(todos) - len(remaining)
        save_todos(remaining)
        print(f"  Cleared {removed} completed todo(s).")
    else:
        save_todos([])
        print(f"  Cleared all {len(todos)} todo(s).")


def cmd_edit(args) -> None:
    """Edit a todo's text."""
    todos = load_todos()
    for t in todos:
        if t["id"] == args.id:
            old_text = t["text"]
            t["text"] = args.text
            if args.priority:
                t["priority"] = args.priority
            save_todos(todos)
            print(f"  Updated #{t['id']}: '{old_text}' -> '{t['text']}'")
            return
    print(f"  Todo #{args.id} not found.")


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit todo",
        description="Manage a local todo list from the terminal.",
    )
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", help="Todo text")
    p_add.add_argument("-p", "--priority", choices=["high", "medium", "low", "none"],
                       default="none", help="Priority level")
    p_add.add_argument("-t", "--tag", action="append", help="Add a tag")

    # list
    p_list = sub.add_parser("list", help="List todos")
    p_list.add_argument("-a", "--all", action="store_true", help="Show completed too")
    p_list.add_argument("-t", "--tag", help="Filter by tag")

    # done
    p_done = sub.add_parser("done", help="Mark todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")

    # undone
    p_undone = sub.add_parser("undone", help="Mark todo as not done")
    p_undone.add_argument("id", type=int, help="Todo ID")

    # remove
    p_rm = sub.add_parser("remove", help="Remove a todo")
    p_rm.add_argument("id", type=int, help="Todo ID")

    # edit
    p_edit = sub.add_parser("edit", help="Edit a todo")
    p_edit.add_argument("id", type=int, help="Todo ID")
    p_edit.add_argument("text", help="New text")
    p_edit.add_argument("-p", "--priority", choices=["high", "medium", "low", "none"])

    # clear
    p_clear = sub.add_parser("clear", help="Clear todos")
    p_clear.add_argument("--done", action="store_true",
                         help="Only clear completed todos")

    args = parser.parse_args(argv)

    if not args.command:
        # Default to list
        args.all = False
        args.tag = None
        cmd_list(args)
        return 0

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "undone": cmd_undone,
        "remove": cmd_remove,
        "edit": cmd_edit,
        "clear": cmd_clear,
    }
    commands[args.command](args)
    return 0
