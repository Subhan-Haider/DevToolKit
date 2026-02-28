"""Main CLI entry point for DevToolKit."""

import sys
import textwrap

BANNER = r"""
  ____             _____           _ _  ___ _   
 |  _ \  _____   _|_   _|__   ___ | | |/ (_) |_ 
 | | | |/ _ \ \ / / | |/ _ \ / _ \| | ' /| | __|
 | |_| |  __/\ V /  | | (_) | (_) | | . \| | |_ 
 |____/ \___| \_/   |_|\___/ \___/|_|_|\_\_|\__|
                                          v1.0.0
"""

TOOLS = {
    "organize":  "Organize files in a directory by type/extension",
    "dupes":     "Find duplicate files by content hash",
    "password":  "Generate strong, customizable passwords",
    "convert":   "Convert between JSON and CSV formats",
    "search":    "Search for text/regex patterns in files",
    "sysinfo":   "Display detailed system information",
    "todo":      "Manage a local todo list from the terminal",
    "hash":      "Compute MD5/SHA1/SHA256 hashes for files & text",
    "timestamp": "Convert between Unix timestamps & date formats",
    "serve":     "Quick HTTP file server with styled directory listing",
    "regex":     "Test regex patterns interactively",
    "snippet":   "Save, retrieve & search reusable code snippets",
    "encode":    "Base64, URL, hex, HTML, JWT encode/decode",
    "diff":      "Compare two files and show differences",
    "lorem":     "Generate placeholder text (Lorem Ipsum)",
    "ai":        "AI assistant powered by Ollama (local LLM)",
    "ui":        "Launch desktop GUI for running DevToolKit tools",
}


def print_help():
    print(BANNER)
    print("  Usage:  python -m devtoolkit <tool> [options]\n")
    print("  Available tools:\n")
    for name, desc in TOOLS.items():
        print(f"    {name:<12} {desc}")
    print()
    print("  Run  python -m devtoolkit <tool> --help  for tool-specific help.\n")


def main(argv=None):
    argv = argv or sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print_help()
        return 0

    tool = argv[0].lower()
    tool_argv = argv[1:]

    if tool == "organize":
        from devtoolkit.tools.file_organizer import run
    elif tool == "dupes":
        from devtoolkit.tools.duplicate_finder import run
    elif tool == "password":
        from devtoolkit.tools.password_gen import run
    elif tool == "convert":
        from devtoolkit.tools.converter import run
    elif tool == "search":
        from devtoolkit.tools.text_search import run
    elif tool == "sysinfo":
        from devtoolkit.tools.sysinfo import run
    elif tool == "todo":
        from devtoolkit.tools.todo_manager import run
    elif tool == "hash":
        from devtoolkit.tools.hash_calc import run
    elif tool == "timestamp":
        from devtoolkit.tools.timestamp import run
    elif tool == "serve":
        from devtoolkit.tools.http_server import run
    elif tool == "regex":
        from devtoolkit.tools.regex_tester import run
    elif tool == "snippet":
        from devtoolkit.tools.snippet_mgr import run
    elif tool == "encode":
        from devtoolkit.tools.encoder import run
    elif tool == "diff":
        from devtoolkit.tools.file_diff import run
    elif tool == "lorem":
        from devtoolkit.tools.lorem import run
    elif tool == "ai":
        from devtoolkit.tools.ai_chat import run
    elif tool == "ui":
        from devtoolkit.ui import run
    else:
        print(f"  Unknown tool: '{tool}'. Run with --help to see available tools.")
        return 1

    return run(tool_argv)
