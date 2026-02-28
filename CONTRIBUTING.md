# Contributing to DevToolKit

Thank you for considering contributing to DevToolKit!

## Quick Start

```bash
# Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/devtoolkit.git
cd devtoolkit

# Create a branch
git checkout -b feature/my-new-tool

# Make changes and test
python -m devtoolkit --help
python -m devtoolkit <your-tool> --help

# Commit and push
git add .
git commit -m "Add my-tool: brief description"
git push origin feature/my-new-tool

# Open a Pull Request on GitHub
```

## Adding a New Tool

1. **Create the tool file:** `devtoolkit/tools/my_tool.py`

```python
"""
My Tool — Short description.

Usage:
    python -m devtoolkit mytool [args]
"""

import argparse


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit mytool",
        description="What my tool does.",
    )
    parser.add_argument("input", help="Input argument")
    parser.add_argument("--flag", action="store_true", help="Optional flag")
    args = parser.parse_args(argv)

    # Your logic here
    print(f"  Result: {args.input}")
    return 0
```

2. **Register in `devtoolkit/cli.py`:**
   - Add to the `TOOLS` dict
   - Add an `elif` in the dispatch block

3. **Test locally:**
```bash
python -m devtoolkit mytool --help
python -m devtoolkit mytool "test input"
```

## Guidelines

- **Zero dependencies** — only use Python's standard library
- **Python 3.10+** — use modern type hints (`list[str]`, `dict[str, int]`, `X | Y`)
- **Follow the pattern** — use `argparse`, return `int` from `run()`, prefix output with `  ` (2 spaces)
- **Be cross-platform** — test on Windows if possible; avoid Unix-only paths
- **Add `--help`** — every tool must have clear help text

## Code Style

- Use descriptive function names
- Add a module-level docstring with usage examples
- Output should look clean in a terminal (2-space indent, separator lines)
- Use `print()` with `f""` strings for output
- Return `0` for success, `1` for errors

## Commit Messages

```
Add <tool-name>: short description
Fix <tool-name>: what was fixed
Improve <tool-name>: what was improved
Docs: what documentation changed
CI: what workflow changed
```
