# DevToolKit

A Swiss-army-knife CLI productivity toolkit for developers. **Zero dependencies** — uses only Python's standard library.

```
  ____             _____           _ _  ___ _   
 |  _ \  _____   _|_   _|__   ___ | | |/ (_) |_ 
 | | | |/ _ \ \ / / | |/ _ \ / _ \| | ' /| | __|
 | |_| |  __/\ V /  | | (_) | (_) | | . \| | |_ 
 |____/ \___| \_/   |_|\___/ \___/|_|_|\_\_|\__|
```

## Quick Start

### Option A: Python (source)
```bash
cd <project-directory>
python -m devtoolkit --help
```

### Option B: Standalone .exe (no Python needed)
Download the latest `.exe` from [Releases](https://github.com/YOUR_USERNAME/devtoolkit/releases), then:

```bash
# Windows
devtoolkit.exe --help
devtoolkit.exe password --count 3
devtoolkit.exe sysinfo

# Linux / macOS
chmod +x devtoolkit-linux-x64
./devtoolkit-linux-x64 --help
```

### Build .exe Locally
```bash
pip install pyinstaller
pyinstaller devtoolkit.spec --noconfirm
# Output: dist/devtoolkit.exe (Windows) or dist/devtoolkit (Linux/macOS)
./dist/devtoolkit --help
```

## 15 Tools Included

### 1. File Organizer — `organize`
Automatically sorts files into folders by type (Images, Documents, Code, etc.)

```bash
# Preview what would happen (safe)
python -m devtoolkit organize ~/Downloads --dry-run

# Actually organize
python -m devtoolkit organize ~/Downloads

# Oops! Undo it
python -m devtoolkit organize ~/Downloads --undo
```

### 2. Duplicate File Finder — `dupes`
Finds duplicate files by SHA-256 content hash (not just name).

```bash
# Scan current directory
python -m devtoolkit dupes .

# Scan recursively with interactive delete
python -m devtoolkit dupes ~/Documents --delete

# Skip tiny files
python -m devtoolkit dupes . --min-size 1024
```

### 3. Password Generator — `password`
Generate cryptographically secure passwords and passphrases.

```bash
# Generate 5 passwords (default)
python -m devtoolkit password

# Custom length, no symbols
python -m devtoolkit password --length 32 --no-symbols

# Generate memorable passphrases
python -m devtoolkit password --passphrase --words 6

# Copy first result to clipboard (Windows)
python -m devtoolkit password --copy
```

### 4. JSON/CSV Converter — `convert`
Bidirectional conversion between JSON and CSV formats.

```bash
# JSON -> CSV
python -m devtoolkit convert data.json

# CSV -> JSON
python -m devtoolkit convert users.csv

# Specify output path
python -m devtoolkit convert data.json --output result.csv
```

### 5. Text Search — `search`
Fast recursive text/regex search across files (like a mini grep/ripgrep).

```bash
# Simple text search
python -m devtoolkit search "TODO" ./src

# Regex search, case-insensitive
python -m devtoolkit search "import\s+\w+" . --regex --ignore-case

# Search only Python files with context
python -m devtoolkit search "def main" . -e .py --context 3

# Just show counts per file
python -m devtoolkit search "error" ./logs --count-only
```

### 6. System Info — `sysinfo`
Display detailed system, Python, network, disk, and dev-tools info.

```bash
python -m devtoolkit sysinfo

# JSON output (great for piping)
python -m devtoolkit sysinfo --json
```

### 7. Todo Manager — `todo`
A persistent todo list that lives in your terminal.

```bash
# Add todos
python -m devtoolkit todo add "Fix login bug" --priority high
python -m devtoolkit todo add "Write tests" --tag work --tag backend

# List active todos
python -m devtoolkit todo list
python -m devtoolkit todo list --all        # include completed

# Complete, edit, remove
python -m devtoolkit todo done 1
python -m devtoolkit todo edit 2 "Write unit tests" --priority medium
python -m devtoolkit todo remove 3

# Cleanup
python -m devtoolkit todo clear --done      # remove completed only
```

### 8. Hash Calculator — `hash`
Compute MD5, SHA1, SHA256, SHA512 hashes for files and text.

```bash
# Hash a file
python -m devtoolkit hash myfile.zip

# Hash a text string
python -m devtoolkit hash "hello world" --text

# Show all algorithms at once
python -m devtoolkit hash document.pdf --all

# Verify a download matches an expected hash
python -m devtoolkit hash installer.exe --compare abc123def456...
```

### 9. Timestamp Converter — `timestamp`
Convert between Unix timestamps, ISO dates, and human-readable formats.

```bash
# Show current time in every format
python -m devtoolkit timestamp

# Unix timestamp -> human readable
python -m devtoolkit timestamp 1709078400

# Date string -> Unix timestamp + all formats
python -m devtoolkit timestamp "2024-02-28"

# Calculate difference between two dates
python -m devtoolkit timestamp --diff "2024-01-01" "2025-01-01"

# Add time to a date
python -m devtoolkit timestamp "2024-01-01" --add 7d
```

### 10. Quick HTTP Server — `serve`
Serve files from a directory with a beautiful dark-themed directory listing.

```bash
# Serve current directory on port 8000
python -m devtoolkit serve

# Serve a specific directory on a custom port
python -m devtoolkit serve ./build --port 3000

# Auto-open browser
python -m devtoolkit serve --open
```

### 11. Regex Tester — `regex`
Test regex patterns against text interactively, with explanations and a cheatsheet.

```bash
# Test a pattern against text
python -m devtoolkit regex "\d{3}-\d{4}" "Call 555-1234"

# Find all matches with groups
python -m devtoolkit regex "(\w+)@(\w+)" "a@b and c@d" --global

# Use a preset pattern
python -m devtoolkit regex email "contact@example.com"

# Show common regex patterns
python -m devtoolkit regex --cheatsheet

# Interactive mode (enter text to test line-by-line)
python -m devtoolkit regex "error|warn" --ignore-case
```

### 12. Snippet Manager — `snippet`
Save, retrieve, and search reusable code snippets from the terminal.

```bash
# Save a snippet from a file
python -m devtoolkit snippet add "docker-compose" --file docker-compose.yml --tag devops

# Save a snippet by typing/pasting it
python -m devtoolkit snippet add "bash-header" --lang bash --desc "Script header"

# Retrieve a snippet
python -m devtoolkit snippet get "docker-compose"

# List and search
python -m devtoolkit snippet list
python -m devtoolkit snippet search "docker"

# Export / Import between machines
python -m devtoolkit snippet export --file my_snippets.json
python -m devtoolkit snippet import my_snippets.json
```

### 13. Encoder/Decoder — `encode`
Base64, URL, hex, HTML, binary, ROT13, JWT, and Unicode encode/decode.

```bash
# Base64 encode/decode
python -m devtoolkit encode base64 "Hello World"
python -m devtoolkit encode base64 "SGVsbG8gV29ybGQ=" --decode

# URL encode
python -m devtoolkit encode url "hello world & more"

# Decode a JWT token
python -m devtoolkit encode jwt "eyJhbGciOiJI..." --decode

# Hex, binary, ROT13
python -m devtoolkit encode hex "hello"
python -m devtoolkit encode binary "AB"
python -m devtoolkit encode rot13 "secret message"

# List all formats
python -m devtoolkit encode --list
```

### 14. File Diff — `diff`
Compare two files with unified diff, side-by-side, or HTML output.

```bash
# Unified diff (like git diff)
python -m devtoolkit diff old.py new.py

# Side-by-side comparison
python -m devtoolkit diff config_v1.yml config_v2.yml --side-by-side

# Generate an HTML diff report
python -m devtoolkit diff before.txt after.txt --html

# Just show stats (no content)
python -m devtoolkit diff a.json b.json --stats
```

### 15. Lorem Ipsum Generator — `lorem`
Generate placeholder text for designs and mockups.

```bash
# Generate 3 paragraphs (default)
python -m devtoolkit lorem

# Generate exactly 50 words
python -m devtoolkit lorem --words 50

# HTML formatted output
python -m devtoolkit lorem --paragraphs 5 --format html

# Save to file
python -m devtoolkit lorem --paragraphs 10 --output placeholder.txt

# Copy to clipboard
python -m devtoolkit lorem --words 100 --copy
```

## Project Structure

```
├── devtoolkit/
│   ├── __init__.py          # Package init
│   ├── __main__.py          # python -m entry point
│   ├── cli.py               # Main CLI router
│   └── tools/
│       ├── __init__.py
│       ├── file_organizer.py    # organize
│       ├── duplicate_finder.py  # dupes
│       ├── password_gen.py      # password
│       ├── converter.py         # convert
│       ├── text_search.py       # search
│       ├── sysinfo.py           # sysinfo
│       ├── todo_manager.py      # todo
│       ├── hash_calc.py         # hash
│       ├── timestamp.py         # timestamp
│       ├── http_server.py       # serve
│       ├── regex_tester.py      # regex
│       ├── snippet_mgr.py       # snippet
│       ├── encoder.py           # encode
│       ├── file_diff.py         # diff
│       └── lorem.py             # lorem
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # CI tests (15 jobs)
│   │   ├── release.yml          # Auto GitHub Release
│   │   ├── build-exe.yml        # Build .exe for Win/Linux/Mac
│   │   ├── scheduled-scan.yml   # Weekly code scan
│   │   ├── pr-check.yml         # PR duplicate/secret scan
│   │   ├── security-scan.yml    # Credential & code scan
│   │   ├── generate-reports.yml # Monthly reports
│   │   ├── organize-uploads.yml # Auto-organize uploads
│   │   └── data-processing.yml  # Convert/generate/hash
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── devtoolkit_app.py        # PyInstaller entry point
├── devtoolkit.spec          # PyInstaller build config
├── .gitignore
├── CONTRIBUTING.md
├── SECURITY.md
├── USAGE.md                 # Complete usage guide
├── LICENSE
└── README.md
```

## Requirements

- **Python 3.10+**
- No external dependencies — 100% standard library

---

## Quick Reference Card

| Tool | Command | Key Flags |
|------|---------|-----------|
| Organize files | `organize [DIR]` | `--dry-run` `--undo` |
| Find duplicates | `dupes [DIR]` | `--delete` `--min-size N` |
| Passwords | `password` | `-l 32` `--passphrase` `--copy` |
| JSON ↔ CSV | `convert FILE` | `-o OUTPUT` `--compact` |
| Text search | `search PAT [DIR]` | `-e .py` `-i` `--regex` `-C 3` |
| System info | `sysinfo` | `--json` |
| Todo list | `todo add/list/done` | `-p high` `-t tag` `--all` |
| Hash files | `hash FILE` | `--all` `--compare HASH` `-t` |
| Timestamps | `timestamp [VAL]` | `--diff A B` `--add 7d` |
| HTTP server | `serve [DIR]` | `-p 3000` `--open` |
| Regex tester | `regex PAT [TEXT]` | `-g` `--cheatsheet` `-e` |
| Snippets | `snippet add/get/list` | `-f FILE` `-t tag` `--raw` |
| Encode/Decode | `encode FMT TEXT` | `-d` `--list` `-f` |
| File diff | `diff A B` | `-s` `--html` `--stats` |
| Lorem ipsum | `lorem` | `-w 50` `-p 5` `-f html` `--copy` |

> Tip: Every tool supports `--help` for full usage details.

---

## Real-World Workflow Examples

### Clean up a messy Downloads folder
```bash
# Preview first
python -m devtoolkit organize ~/Downloads --dry-run
# Looks good — do it
python -m devtoolkit organize ~/Downloads
# Oops, I need that file back
python -m devtoolkit organize ~/Downloads --undo
```

### Verify a downloaded file's integrity
```bash
python -m devtoolkit hash ubuntu-24.04.iso --compare "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
```

### Debug a JWT token from an API response
```bash
python -m devtoolkit encode jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" --decode
```

### Find all TODO comments in a project
```bash
python -m devtoolkit search "TODO|FIXME|HACK|XXX" ./src --regex --ignore-case --count-only
```

### Quick-share files on your local network
```bash
python -m devtoolkit serve ./shared-folder --port 9000 --open
# Anyone on the network can access http://<your-ip>:9000
```

### Convert API response JSON to a spreadsheet
```bash
python -m devtoolkit convert api_response.json --output report.csv
```

### Track your daily tasks
```bash
python -m devtoolkit todo add "Deploy v2.0" --priority high --tag release
python -m devtoolkit todo add "Write changelog" --priority medium --tag docs
python -m devtoolkit todo list
python -m devtoolkit todo done 1
```

### Generate mock content for a website
```bash
python -m devtoolkit lorem --paragraphs 5 --format html --output content.html
```

### Save and reuse a complex command
```bash
python -m devtoolkit snippet add "git-squash" --lang bash --desc "Squash last N commits" --tag git
python -m devtoolkit snippet get "git-squash" --raw | clip
```

### How many days until a deadline?
```bash
python -m devtoolkit timestamp --diff "2026-02-27" "2026-12-31"
```

---

## Keyboard Shortcuts & Tips

| Tip | Description |
|-----|-------------|
| **Tab completion** | Every tool uses `argparse` — compatible with shell auto-complete |
| **Pipe-friendly** | Use `--json`, `--raw`, `--compact` flags to pipe output to other tools |
| **Clipboard** | `--copy` flag available on `password`, `lorem` tools (uses `clip` on Windows) |
| **File or text** | `hash` and `encode` auto-detect files vs text; use `-t`/`--text` to force text mode |
| **Undo support** | `organize --undo` reverts the last file sort using a JSON log |
| **Presets** | `regex email`, `regex url`, etc. — use named presets instead of typing patterns |
| **Persistent data** | `todo` and `snippet` data saved in your home directory (`~/.devtoolkit_*.json`) |

---

## Data Storage

| Tool | File Location | Format |
|------|--------------|--------|
| Todo Manager | `~/.devtoolkit_todos.json` | JSON array |
| Snippet Manager | `~/.devtoolkit_snippets.json` | JSON object |
| File Organizer | `<dir>/_organize_log.json` | JSON (undo log) |

All data is stored as plain JSON — easy to back up, version-control, or edit manually.

---

## Aliases (Optional)

Add these to your PowerShell profile (`$PROFILE`) or `.bashrc` for quicker access:

### PowerShell
```powershell
function dtk { python -m devtoolkit @args }
function todo { python -m devtoolkit todo @args }
function pw { python -m devtoolkit password @args }
function serve { python -m devtoolkit serve @args }
```

### Bash / Zsh
```bash
alias dtk="python -m devtoolkit"
alias todo="python -m devtoolkit todo"
alias pw="python -m devtoolkit password"
alias serve="python -m devtoolkit serve"
```

Then use: `dtk hash myfile.zip --all` or `todo add "Fix bug" -p high`

---

## FAQ

**Q: Does this need pip install?**
A: No. Just clone/copy the `devtoolkit/` folder and run `python -m devtoolkit`. Zero external dependencies.

**Q: What Python version do I need?**
A: Python 3.10 or newer (uses `match` syntax, `list[str]` type hints, and walrus operator).

**Q: Where is my todo/snippet data stored?**
A: In your home directory as JSON files (`~/.devtoolkit_todos.json` and `~/.devtoolkit_snippets.json`). They're plain text — safe to back up or sync via cloud storage.

**Q: Can I use this on Linux/macOS?**
A: Yes. Everything is cross-platform. The only Windows-specific feature is `--copy` using `clip.exe`; on Linux, install `xclip` or `xsel` for clipboard support.

**Q: How does the file organizer decide categories?**
A: It maps 80+ file extensions to 9 categories (Images, Documents, Videos, Audio, Archives, Code, Executables, Fonts, Data). Unrecognized extensions go to an "Other" folder.

**Q: Is the HTTP server secure enough for production?**
A: No — `serve` is for local development and LAN file sharing only. It's Python's built-in HTTP server with a styled frontend. Don't expose it to the internet.

**Q: Can I add my own tools?**
A: Yes! Create a new file in `devtoolkit/tools/`, add a `run(argv)` function, and register it in `cli.py`. See any existing tool as a template.

---

## Adding Your Own Tool

1. Create `devtoolkit/tools/my_tool.py`:
```python
import argparse

def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="devtoolkit mytool")
    parser.add_argument("name", help="Your argument")
    args = parser.parse_args(argv)
    
    print(f"  Hello from my tool: {args.name}")
    return 0
```

2. Register it in `devtoolkit/cli.py`:
```python
# Add to the TOOLS dict:
"mytool": "Description of my tool",

# Add to the dispatch block:
elif tool == "mytool":
    from devtoolkit.tools.my_tool import run
```

3. Run it:
```bash
python -m devtoolkit mytool "world"
```

---

## Changelog

### v1.0.0 — Initial Release
- 15 built-in tools
- Zero dependencies — pure Python standard library
- Cross-platform (Windows, macOS, Linux)
- Persistent storage for todos and snippets
- Undo support for file organizer

---

## GitHub Setup & Automation

### Step 1: Create a GitHub Repository

```bash
# Initialize git and push to GitHub
cd devtoolkit-project
git init
git add .
git commit -m "Initial commit: DevToolKit v1.0.0"

# Create repo on GitHub (using GitHub CLI)
gh repo create devtoolkit --public --source=. --push

# OR manually: create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/devtoolkit.git
git branch -M main
git push -u origin main
```

### Step 2: Clone & Use on Another Machine

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/devtoolkit.git
cd devtoolkit

# Use immediately — no install needed
python -m devtoolkit --help
```

---

## GitHub Actions (CI/CD Automation)

DevToolKit ships with **9 GitHub Actions workflows** in `.github/workflows/`:

| # | Workflow | File | Trigger | Purpose |
|---|----------|------|---------|---------|
| 1 | **CI** | `ci.yml` | Push / PR | Lint + test all 15 tools on 15 environments |
| 2 | **Release** | `release.yml` | `v*.*.*` tag | Create GitHub Release with archives |
| 3 | **Build EXE** | `build-exe.yml` | `v*.*.*` tag / manual | Build Win/Mac/Linux executables |
| 4 | **Scheduled Scan** | `scheduled-scan.yml` | Weekly (Mon 8am) | Find TODOs, debug prints, duplicates |
| 5 | **PR Check** | `pr-check.yml` | Pull Request | Duplicate check, TODO scan, secret scan |
| 6 | **Security Scan** | `security-scan.yml` | Push / PR / Weekly | Credential & dangerous function scan |
| 7 | **Generate Reports** | `generate-reports.yml` | Monthly / Manual | System info, code stats, hash manifests |
| 8 | **Organize Uploads** | `organize-uploads.yml` | PR to `uploads/` | Preview file organization |
| 9 | **Data Processing** | `data-processing.yml` | Manual | Convert data, generate content, hash files |

### 1. CI — `ci.yml`
Runs on every push and pull request. Tests all 15 tools across Python 3.10–3.14 × Ubuntu, Windows, macOS (15 environments).

### 2. Release — `release.yml`
Creates a GitHub Release when you push a version tag:
```bash
git tag v1.0.0 && git push origin v1.0.0
```

### 3. Build EXE — `build-exe.yml`
Builds standalone executables for **Windows x64, Linux x64, macOS ARM64** via PyInstaller. Runs with releases or manually from the Actions tab.

### 4. Scheduled Scan — `scheduled-scan.yml`
Weekly code health check: finds TODO/FIXME comments, debug prints, duplicate files, syntax errors.

### 5. PR Check — `pr-check.yml` *(NEW)*
Runs on every pull request:
- Scans for **duplicate files** in the repo
- Finds **TODO/FIXME** in changed Python files
- Checks for **hardcoded secrets** patterns
- Shows **diff stats** for changed files

### 6. Security Scan — `security-scan.yml` *(NEW)*
Runs on push to main, PRs, and every Wednesday:
- Scans for hardcoded passwords, API keys, tokens
- Detects dangerous functions (`eval()`, `exec()`, `os.system()`)
- Finds debug leftovers (`breakpoint()`, `pdb`)
- Checks for large files (>1MB)
- Generates source file hash manifest

### 7. Generate Reports — `generate-reports.yml` *(NEW)*
Runs monthly and on-demand. Choose report type:
- **full-report** — all reports combined
- **system-info** — CI environment details (JSON)
- **code-stats** — file counts, LOC, TODOs, duplicates
- **hash-manifest** — SHA-256 of all Python source files

Reports are uploaded as downloadable artifacts (90-day retention).

### 8. Organize Uploads — `organize-uploads.yml` *(NEW)*
Triggers when PRs touch `uploads/` or `assets/` directories:
- Shows dry-run file organization preview
- Checks for duplicate uploads
- Hashes all uploaded files

### 9. Data Processing — `data-processing.yml` *(NEW)*
Manual-dispatch workflow with 5 actions:
- **convert-json-to-csv** / **convert-csv-to-json** — File format conversion
- **generate-placeholder** — Lorem ipsum in HTML/JSON/TXT/Markdown
- **generate-passwords** — Secure passwords and passphrases
- **hash-directory** — Hash all files in a directory

### How to Enable GitHub Actions

1. Push the `.github/workflows/` folder to your repo
2. Go to the **Actions** tab on your GitHub repo
3. Workflows run automatically — no configuration needed
4. Manual workflows: Actions tab → select workflow → **Run workflow**

View results at `https://github.com/YOUR_USERNAME/devtoolkit/actions`

> **Full usage guide:** See [USAGE.md](USAGE.md) for detailed instructions, every flag, and workflow recipes.

---

## GitHub Actions — Using DevToolKit in Your Own Workflows

You can use DevToolKit as a step in any GitHub Actions workflow:

### Example: Verify file hashes in CI
```yaml
name: Verify Assets
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Verify checksums
        run: |
          python -m devtoolkit hash dist/app.zip --compare "${{ vars.EXPECTED_HASH }}"
```

### Example: Find duplicate assets in CI
```yaml
name: Check Duplicates
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Scan for duplicate files
        run: python -m devtoolkit dupes ./assets --min-size 1024
```

### Example: Generate placeholder content during build
```yaml
name: Build Site
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Generate mock content
        run: |
          python -m devtoolkit lorem --paragraphs 10 --format html --output public/placeholder.html
      - name: Convert data
        run: |
          python -m devtoolkit convert data/seed.json --output data/seed.csv
```

### Example: Search for code quality issues
```yaml
name: Code Quality
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Find TODOs and FIXMEs
        run: python -m devtoolkit search "TODO|FIXME|HACK|XXX" ./src --regex --count-only
      - name: Check for debug prints
        run: python -m devtoolkit search "print(" ./src -e .py --count-only
```

---

## GitHub Badges

Add these to the top of your README after pushing:

```markdown
![CI](https://github.com/YOUR_USERNAME/devtoolkit/actions/workflows/ci.yml/badge.svg)
![Security Scan](https://github.com/YOUR_USERNAME/devtoolkit/actions/workflows/security-scan.yml/badge.svg)
![Build EXE](https://github.com/YOUR_USERNAME/devtoolkit/actions/workflows/build-exe.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![No Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)
![Tools](https://img.shields.io/badge/tools-15-orange)
![Workflows](https://img.shields.io/badge/workflows-9-purple)
```

---

## GitHub Releases — How to Publish

### Step-by-step:

```bash
# 1. Update version in __init__.py and cli.py
# 2. Commit changes
git add .
git commit -m "Release v1.1.0"

# 3. Create an annotated tag
git tag -a v1.1.0 -m "v1.1.0 - Added new tools"

# 4. Push code and tag
git push origin main
git push origin v1.1.0

# 5. GitHub Actions automatically:
#    - Runs all tests across 15 jobs
#    - Builds standalone .exe for Windows, Linux, macOS
#    - Creates a GitHub Release
#    - Attaches .exe + .zip + .tar.gz downloads
```

### Manual Release (via GitHub CLI)
```bash
gh release create v1.1.0 --title "DevToolKit v1.1.0" --notes "- Added new tools
- Bug fixes
- Performance improvements"
```

---

## Contributing via GitHub

### Fork & Pull Request Workflow

```bash
# 1. Fork the repo on GitHub (click "Fork" button)

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/devtoolkit.git
cd devtoolkit

# 3. Create a feature branch
git checkout -b feature/my-new-tool

# 4. Make changes, add your tool
# 5. Test it
python -m devtoolkit mytool --help

# 6. Commit and push
git add .
git commit -m "Add mytool: description of what it does"
git push origin feature/my-new-tool

# 7. Open a Pull Request on GitHub
gh pr create --title "Add mytool" --body "Description of changes"
```

### Branch Protection (Recommended)

In your repo settings (`Settings > Branches > Branch protection rules`), add a rule for `main`:

- [x] Require a pull request before merging
- [x] Require status checks to pass (select the CI workflow)
- [x] Require branches to be up to date before merging

This ensures all changes pass CI before merging.

---

## GitHub Issues — Bug Reports & Feature Requests

Use the included issue templates (`.github/ISSUE_TEMPLATE/`):

```bash
# Report a bug (using GitHub CLI)
gh issue create --title "Bug: organize fails on symlinks" --label bug

# Request a feature
gh issue create --title "Feature: add XML-to-JSON converter" --label enhancement
```

---

## License

MIT — free for personal and commercial use. See [LICENSE](LICENSE).

## Security

See [SECURITY.md](SECURITY.md) for:
- Responsible vulnerability reporting
- Per-tool security considerations (`serve`, `password`, `hash`, `encode`, etc.)
- Data storage safety notes
- General security posture (zero deps, no network, no telemetry, no eval)

---

<p align="center">
  Built with Python. No dependencies. Just productivity.<br>
  <b>DevToolKit v1.0.0</b>
</p>