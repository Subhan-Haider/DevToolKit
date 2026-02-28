# DevToolKit — Complete Usage Guide

A hands-on guide covering every tool, every flag, and real-world recipes.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Tool Reference](#tool-reference)
   - [organize — Sort files into folders](#1-organize)
   - [dupes — Find duplicate files](#2-dupes)
   - [password — Generate passwords](#3-password)
   - [convert — JSON ↔ CSV](#4-convert)
   - [search — Search text in files](#5-search)
   - [sysinfo — System information](#6-sysinfo)
   - [todo — Task manager](#7-todo)
   - [hash — File/text hashing](#8-hash)
   - [timestamp — Date/time converter](#9-timestamp)
   - [serve — HTTP file server](#10-serve)
   - [regex — Regex tester](#11-regex)
   - [snippet — Code snippet manager](#12-snippet)
   - [encode — Encode/decode text](#13-encode)
   - [diff — Compare files](#14-diff)
   - [lorem — Placeholder text](#15-lorem)
   - [ai — AI assistant (Ollama)](#16-ai)
4. [Workflow Recipes](#workflow-recipes)
5. [GitHub Actions Usage](#github-actions-usage)
6. [Tips & Tricks](#tips--tricks)

---

## Installation

### Option A: Run from source (recommended for development)

```bash
# Clone or download the project
git clone https://github.com/YOUR_USERNAME/devtoolkit.git
cd devtoolkit

# Run directly — no pip install needed
python -m devtoolkit --help
```

### Option B: Standalone executable

Download the latest `.exe` / binary from [Releases](https://github.com/YOUR_USERNAME/devtoolkit/releases):

```bash
# Windows
devtoolkit.exe --help

# Linux / macOS
chmod +x devtoolkit
./devtoolkit --help
```

### Option C: Add shell aliases

**PowerShell** (add to `$PROFILE`):
```powershell
function dtk { python -m devtoolkit @args }
```

**Bash / Zsh** (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias dtk="python -m devtoolkit"
```

Now use `dtk organize .` instead of `python -m devtoolkit organize .`.

---

## Quick Start

```bash
# See all tools
python -m devtoolkit --help

# Get help for a specific tool
python -m devtoolkit organize --help

# Try a few tools right now:
python -m devtoolkit sysinfo                    # Show system info
python -m devtoolkit password --length 20       # Generate a password
python -m devtoolkit timestamp now              # Current time in all formats
python -m devtoolkit lorem --words 50           # Generate placeholder text
```

---

## Tool Reference

### 1. organize

Sort files into categorized subfolders (Images, Documents, Code, etc.).

```bash
# Organize current directory
python -m devtoolkit organize .

# Preview without moving anything
python -m devtoolkit organize ~/Downloads --dry-run

# Undo the last organization (restores original locations)
python -m devtoolkit organize ~/Downloads --undo
```

**Categories:** Images, Documents, Code, Archives, Audio, Video, Data, Fonts, Other

**Flags:**
| Flag | Description |
|------|-------------|
| `--dry-run` | Preview moves without executing |
| `--undo` | Reverse the last organize operation |

---

### 2. dupes

Find duplicate files by content hash (SHA-256).

```bash
# Find duplicates in current directory
python -m devtoolkit dupes .

# Only check files larger than 1KB
python -m devtoolkit dupes . --min-size 1024

# Find and interactively delete duplicates
python -m devtoolkit dupes ~/Photos --delete
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--min-size N` | Skip files smaller than N bytes |
| `--delete` | Interactively choose duplicates to delete |

---

### 3. password

Generate cryptographically secure passwords and passphrases.

```bash
# Default: 16-char password
python -m devtoolkit password

# Custom length
python -m devtoolkit password --length 32

# Multiple passwords
python -m devtoolkit password --count 5 --length 24

# Exclude ambiguous characters (0/O, 1/l/I)
python -m devtoolkit password --no-ambiguous

# Passphrase mode (e.g., correct-horse-battery-staple)
python -m devtoolkit password --passphrase --words 5

# Copy to clipboard (Windows/macOS)
python -m devtoolkit password --copy
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--length N` | Password length (default: 16) |
| `--count N` | Number of passwords to generate |
| `--no-ambiguous` | Remove confusing characters |
| `--passphrase` | Generate words-based passphrase |
| `--words N` | Number of words in passphrase |
| `--separator` | Passphrase word separator (default: `-`) |
| `--copy` | Copy to clipboard |

---

### 4. convert

Convert between JSON and CSV formats.

```bash
# JSON → CSV
python -m devtoolkit convert data.json

# CSV → JSON (auto-detects format)
python -m devtoolkit convert data.csv

# Custom output path
python -m devtoolkit convert data.json --output result.csv

# Handle nested objects (auto-flattened)
python -m devtoolkit convert nested-api-response.json
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--output PATH` | Custom output file path |

---

### 5. search

Fast recursive text search (like grep, but friendlier).

```bash
# Simple text search
python -m devtoolkit search "TODO" .

# Regex search
python -m devtoolkit search "def \w+\(" . --regex

# Only in Python files
python -m devtoolkit search "import os" . -e .py

# Case-insensitive with context
python -m devtoolkit search "error" /var/log --ignore-case --context 3

# Count matches only
python -m devtoolkit search "TODO" . --count-only
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--regex` | Treat pattern as regular expression |
| `--ignore-case` / `-i` | Case-insensitive search |
| `-e EXT` | Filter by file extension (e.g., `-e .py`) |
| `--context N` | Show N lines of context around matches |
| `--count-only` | Only show count of matches |

---

### 6. sysinfo

Display system, Python, network, and disk information.

```bash
# Full system report
python -m devtoolkit sysinfo

# JSON output (great for CI/CD)
python -m devtoolkit sysinfo --json

# Pipe to a file for logging
python -m devtoolkit sysinfo --json > system-report.json
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--json` | Output as JSON (machine-readable) |

---

### 7. todo

Persistent task manager stored at `~/.devtoolkit_todos.json`.

```bash
# Add a task
python -m devtoolkit todo add "Fix login bug" --priority high --tag backend

# List all tasks
python -m devtoolkit todo list

# Filter by tag or priority
python -m devtoolkit todo list --tag backend
python -m devtoolkit todo list --priority high

# Mark done
python -m devtoolkit todo done 1

# Mark undone
python -m devtoolkit todo undone 1

# Edit a task
python -m devtoolkit todo edit 1 --text "Fix login and signup bugs"

# Remove completed tasks
python -m devtoolkit todo clear
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| `add TEXT` | Add a new task |
| `list` | List all tasks |
| `done ID` | Mark task as done |
| `undone ID` | Mark task as not done |
| `edit ID` | Edit task text/priority/tag |
| `clear` | Remove completed tasks |

**Flags:** `--priority` (low/medium/high), `--tag TAG`

---

### 8. hash

Calculate file or text hashes.

```bash
# Default (SHA-256)
python -m devtoolkit hash myfile.zip

# Specific algorithm
python -m devtoolkit hash myfile.zip --algo md5

# All algorithms at once
python -m devtoolkit hash myfile.zip --all

# Hash a text string
python -m devtoolkit hash --text "hello world"

# Verify a known hash
python -m devtoolkit hash myfile.zip --compare abc123def456...
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--algo ALG` | md5, sha1, sha256, sha512 |
| `--all` | Calculate all algorithms |
| `--text STRING` | Hash a text string instead of file |
| `--compare HASH` | Verify against expected hash |

---

### 9. timestamp

Convert between timestamp formats and do date math.

```bash
# Current time in all formats
python -m devtoolkit timestamp now

# Unix → human-readable
python -m devtoolkit timestamp 1700000000

# ISO → Unix
python -m devtoolkit timestamp "2024-06-15T10:30:00"

# Difference between two dates
python -m devtoolkit timestamp "2024-01-01" --diff "2024-12-31"

# Add duration to a date
python -m devtoolkit timestamp "2024-01-01" --add "30d"
python -m devtoolkit timestamp now --add "2h30m"
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--diff DATE` | Show difference between two dates |
| `--add DURATION` | Add duration (e.g., `30d`, `2h`, `45m`, `2h30m`) |

---

### 10. serve

Start a local HTTP file server with styled directory listing.

```bash
# Serve current directory on port 8000
python -m devtoolkit serve

# Custom port and directory
python -m devtoolkit serve /path/to/files --port 3000

# Auto-open browser
python -m devtoolkit serve . --open
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--port N` | Port number (default: 8000) |
| `--open` | Open browser automatically |

**Note:** For local development only — not a production server.

---

### 11. regex

Interactive regex tester with presets and cheat sheet.

```bash
# Interactive mode
python -m devtoolkit regex

# Test a pattern against text
python -m devtoolkit regex "(\d{3})-(\d{4})" --test "Call 555-1234 today"

# Use preset patterns
python -m devtoolkit regex --preset email --test "contact john@example.com"

# Find all matches
python -m devtoolkit regex "\b\w+@\w+\.\w+\b" --test "a@b.c and d@e.f" --global

# Show cheat sheet
python -m devtoolkit regex --cheatsheet

# Explain a pattern
python -m devtoolkit regex "^[A-Za-z0-9._%+-]+@" --explain
```

**Presets:** `email`, `url`, `ipv4`, `phone`, `date`, `hex-color`

**Flags:**
| Flag | Description |
|------|-------------|
| `--test TEXT` | Text to test against |
| `--preset NAME` | Use built-in pattern |
| `--global` | Find all matches |
| `--cheatsheet` | Show regex cheat sheet |
| `--explain` | Explain the pattern |

---

### 12. snippet

Persistent code snippet manager stored at `~/.devtoolkit_snippets.json`.

```bash
# Add a snippet
python -m devtoolkit snippet add "python-main" --lang python --code 'if __name__ == "__main__":\n    main()'

# Add from a file
python -m devtoolkit snippet add "config-template" --lang yaml --file config.example.yml

# Retrieve a snippet
python -m devtoolkit snippet get python-main

# List all snippets
python -m devtoolkit snippet list

# Search snippets
python -m devtoolkit snippet search "main"

# Export all to JSON
python -m devtoolkit snippet export my-snippets.json

# Import from JSON
python -m devtoolkit snippet import shared-snippets.json

# Remove a snippet
python -m devtoolkit snippet remove python-main
```

---

### 13. encode

Encode and decode text in various formats.

```bash
# Base64 encode
python -m devtoolkit encode base64 "Hello World"

# Base64 decode
python -m devtoolkit encode base64 "SGVsbG8gV29ybGQ=" --decode

# URL encode
python -m devtoolkit encode url "hello world & more"

# HTML encode
python -m devtoolkit encode html '<script>alert("xss")</script>'

# Hex encode
python -m devtoolkit encode hex "Hello"

# Binary
python -m devtoolkit encode binary "Hi"

# ROT13
python -m devtoolkit encode rot13 "Secret Message"

# JWT decode (no verification — inspection only)
python -m devtoolkit encode jwt "eyJhbGciOi..."

# Unicode escape
python -m devtoolkit encode unicode "café ☕"
```

**Formats:** `base64`, `url`, `html`, `hex`, `binary`, `rot13`, `jwt`, `unicode`

**Flags:**
| Flag | Description |
|------|-------------|
| `--decode` | Decode instead of encode |

---

### 14. diff

Compare two files with unified or side-by-side diff.

```bash
# Unified diff
python -m devtoolkit diff file1.py file2.py

# Side-by-side comparison
python -m devtoolkit diff file1.py file2.py --side-by-side

# Generate HTML diff report
python -m devtoolkit diff file1.py file2.py --html

# Show change statistics only
python -m devtoolkit diff file1.py file2.py --stats
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--side-by-side` | Side-by-side comparison |
| `--html` | Generate HTML diff report |
| `--stats` | Show only change statistics |

---

### 15. lorem

Generate placeholder text in multiple formats.

```bash
# Default: 1 paragraph
python -m devtoolkit lorem

# Custom word count
python -m devtoolkit lorem --words 100

# Multiple paragraphs
python -m devtoolkit lorem --paragraphs 5

# Sentence count
python -m devtoolkit lorem --sentences 10

# HTML format
python -m devtoolkit lorem --paragraphs 3 --format html

# JSON format (for API mocking)
python -m devtoolkit lorem --paragraphs 3 --format json

# Markdown format
python -m devtoolkit lorem --words 200 --format markdown

# Word-wrapped for terminal
python -m devtoolkit lorem --paragraphs 2 --format wrapped

# Save to file
python -m devtoolkit lorem --paragraphs 10 --format html --output content.html
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--words N` | Generate N words |
| `--paragraphs N` | Generate N paragraphs |
| `--sentences N` | Generate N sentences |
| `--format FMT` | text, html, json, markdown, wrapped |
| `--output FILE` | Save to file |

---

### 16. ai

AI assistant powered by [Ollama](https://ollama.com) — runs 100% locally.

**Setup:**
```bash
# 1. Install Ollama: https://ollama.com/download
# 2. Start the server
ollama serve

# 3. Pull a model
python -m devtoolkit ai pull llama3
```

**Subcommands:**

```bash
# List available models
python -m devtoolkit ai models

# Pull / download a model
python -m devtoolkit ai pull mistral
python -m devtoolkit ai pull codellama
python -m devtoolkit ai pull llama3

# Interactive chat
python -m devtoolkit ai chat
python -m devtoolkit ai chat -m mistral
python -m devtoolkit ai chat -s "You are a helpful Python tutor"

# Single prompt (non-interactive)
python -m devtoolkit ai chat -p "Explain async/await in Python"

# Ask a question (optionally with file context)
python -m devtoolkit ai ask "What is a binary search tree?"
python -m devtoolkit ai ask "What does this function do?" -f utils.py

# Summarise files
python -m devtoolkit ai summarize README.md
python -m devtoolkit ai summarize src/main.py src/utils.py

# Code review
python -m devtoolkit ai review app.py

# Explain code (instead of review)
python -m devtoolkit ai review app.py --explain

# Generate code
python -m devtoolkit ai generate "merge sort algorithm" --lang python
python -m devtoolkit ai generate "REST API with Express" --lang javascript -o server.js
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| `models` | List locally available models |
| `pull NAME` | Download a model |
| `chat` | Interactive chat (or single prompt with `-p`) |
| `ask QUESTION` | Ask a single question |
| `summarize FILES` | Summarise one or more files |
| `review FILE` | Code review (or `--explain`) |
| `generate DESC` | Generate code from description |

**Flags:**
| Flag | Description |
|------|-------------|
| `-m MODEL` | Model name (default: `llama3`) |
| `-p PROMPT` | Single prompt for chat |
| `-s SYSTEM` | System prompt to set AI behaviour |
| `-f FILE` | Include file as context (`ask` command) |
| `--explain` | Explain instead of review |
| `-l LANG` | Language for code generation |
| `-o FILE` | Save generated code to file |

**Chat commands:** `/quit`, `/clear`, `/model`

**Environment:** Set `OLLAMA_HOST` to use a remote server (default: `http://localhost:11434`)

---

## Workflow Recipes

### Recipe 1: Clean up a messy Downloads folder

```bash
# Step 1: Preview what will happen
python -m devtoolkit organize ~/Downloads --dry-run

# Step 2: Find and optionally delete duplicates
python -m devtoolkit dupes ~/Downloads --delete

# Step 3: Actually organize the files
python -m devtoolkit organize ~/Downloads

# Step 4: Oops, want to undo?
python -m devtoolkit organize ~/Downloads --undo
```

### Recipe 2: Verify a file download

```bash
# Hash the downloaded file
python -m devtoolkit hash download.iso --algo sha256

# Or compare directly with a known hash
python -m devtoolkit hash download.iso --compare "expected_sha256_hash_here"
```

### Recipe 3: Find and fix TODOs in your codebase

```bash
# Find all TODO comments in Python files
python -m devtoolkit search "TODO|FIXME|HACK|XXX" src/ --regex -e .py

# Track them as tasks
python -m devtoolkit todo add "Fix: login validation TODO" --priority high --tag backend
python -m devtoolkit todo add "Fix: caching FIXME" --priority medium --tag performance

# Check off as you complete them
python -m devtoolkit todo done 1
```

### Recipe 4: Quick API data processing

```bash
# Save API response to JSON
curl -s https://api.example.com/users > users.json

# Convert to CSV for spreadsheet use
python -m devtoolkit convert users.json --output users.csv

# Need it back as JSON?
python -m devtoolkit convert users.csv --output users-clean.json
```

### Recipe 5: Share files with a colleague on the same network

```bash
# Start a file server (shows your local IP)
python -m devtoolkit serve ~/SharedFiles --port 9000 --open

# Share the URL with your colleague: http://192.168.1.x:9000
```

### Recipe 6: Code review preparation

```bash
# Compare old vs new implementation
python -m devtoolkit diff old_handler.py new_handler.py --side-by-side

# Generate an HTML diff report to share
python -m devtoolkit diff old_handler.py new_handler.py --html

# Check for any leftover debug prints
python -m devtoolkit search "print(" src/ -e .py --count-only
```

### Recipe 7: Quick secret generation for config files

```bash
# Generate a strong secret key
python -m devtoolkit password --length 64 --copy

# Generate multiple API keys
python -m devtoolkit password --count 5 --length 32

# Need memorable passphrases for team members?
python -m devtoolkit password --passphrase --words 5 --count 10
```

### Recipe 8: Date math for project planning

```bash
# How many days until deadline?
python -m devtoolkit timestamp now --diff "2025-03-01"

# What date is 90 days from now?
python -m devtoolkit timestamp now --add "90d"

# Convert a Unix timestamp from logs
python -m devtoolkit timestamp 1700000000
```

### Recipe 9: Build a quick mockup with placeholder content

```bash
# Generate dummy text for a landing page
python -m devtoolkit lorem --paragraphs 3 --format html --output mockup.html

# Generate JSON for API mock
python -m devtoolkit lorem --paragraphs 5 --format json --output mock-data.json

# Generate markdown for docs
python -m devtoolkit lorem --words 300 --format markdown --output draft.md
```

### Recipe 10: Regex debugging session

```bash
# Show the cheat sheet first
python -m devtoolkit regex --cheatsheet

# Test your email regex
python -m devtoolkit regex "^[\w.+-]+@[\w-]+\.[\w.]+$" --test "user@example.com"

# Find all URLs in a text
python -m devtoolkit regex --preset url --test "Visit https://example.com or http://test.org" --global

# Enter interactive mode for experimentation
python -m devtoolkit regex
```

---

## GitHub Actions Usage

DevToolKit ships with **9 GitHub Actions workflows** that automate common tasks.

### Workflow Overview

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `ci.yml` | Push / PR | Lint + test all 16 tools across 15 environments |
| **Release** | `release.yml` | Version tag | Create GitHub Release with changelog |
| **Build EXE** | `build-exe.yml` | Version tag | Build standalone executables (Win/Mac/Linux) |
| **Scheduled Scan** | `scheduled-scan.yml` | Weekly (Mon) | Find TODOs, debug prints, duplicates |
| **PR Check** | `pr-check.yml` | Pull Request | Duplicate check, TODO scan, secret scan |
| **Security Scan** | `security-scan.yml` | Push / PR / Weekly | Credential scan, dangerous functions, large files |
| **Generate Reports** | `generate-reports.yml` | Monthly / Manual | System info, code stats, hash manifests |
| **Organize Uploads** | `organize-uploads.yml` | PR to uploads/ | Preview file organization, check duplicates |
| **Data Processing** | `data-processing.yml` | Manual | Convert data, generate content, hash directories |

### How to use each workflow

#### CI — Automatic on every push and PR

No setup needed. Runs automatically when you push code or create a pull request.

```bash
git add . && git commit -m "feat: new feature" && git push
# → CI workflow tests all 15 tools automatically
```

#### Release — Tag a version to publish

```bash
# Update version in devtoolkit/__init__.py
git add . && git commit -m "release: v1.1.0"
git tag v1.1.0
git push origin main --tags
# → Creates a GitHub Release with source archives + release notes
```

#### Build EXE — Triggered by version tags

Runs automatically with the release workflow. You can also trigger manually:

1. Go to **Actions** → **Build Executable**
2. Click **Run workflow**
3. Download executables from the Release page or Artifacts

#### PR Check — Automatic on PRs

When you open a PR, this workflow:
- Scans for duplicate files
- Finds TODO/FIXME in changed files
- Checks for hardcoded secrets

#### Security Scan — Automatic + manual

Runs on every push to `main`, every PR, and weekly. Also available manually:

1. Go to **Actions** → **Security Scan**
2. Click **Run workflow**
3. Check the **Summary** tab for results

#### Generate Reports — Monthly + manual

```bash
# Trigger manually from GitHub Actions tab:
# Choose: full-report, system-info, code-stats, or hash-manifest
# Download the report from Artifacts
```

#### Data Processing — Manual dispatch

1. Go to **Actions** → **Convert & Process Data**
2. Choose an action: convert JSON/CSV, generate content, create passwords, hash files
3. Fill in the input file path if needed
4. Reports and generated files appear in Artifacts

### Setting up the repository

```bash
# 1. Initialize git
git init
git add .
git commit -m "initial commit: DevToolKit v1.0.0"

# 2. Create GitHub repo and push
gh repo create devtoolkit --public --push
# or:
git remote add origin https://github.com/YOUR_USERNAME/devtoolkit.git
git push -u origin main

# 3. Workflows run automatically — check the Actions tab!

# 4. To create your first release:
git tag v1.0.0
git push origin v1.0.0
```

---

## Tips & Tricks

### Chaining tools with shell pipes

```bash
# Generate a password and hash it
python -m devtoolkit password | python -m devtoolkit hash --text "$(cat)"

# Find TODOs and count them
python -m devtoolkit search "TODO" src/ --count-only

# Convert API response piped from curl
curl -s api.example.com/data > data.json && python -m devtoolkit convert data.json
```

### Data storage locations

| Data | Location |
|------|----------|
| Todos | `~/.devtoolkit_todos.json` |
| Snippets | `~/.devtoolkit_snippets.json` |
| File organizer undo log | `<organized-dir>/.organize_log.json` |

### Performance tips

- `dupes` uses size-based pre-filtering — only files with matching sizes get hashed
- `search` skips binary files automatically
- `hash` streams files in chunks — works on multi-GB files
- `organize --dry-run` is instant — always preview first

### Portable usage

The standalone executable works anywhere without Python installed:

```bash
# USB drive workflow
E:\devtoolkit.exe organize D:\messy-folder
E:\devtoolkit.exe hash important-file.pdf --all
E:\devtoolkit.exe serve D:\shared-files --port 9000
```

---

*Generated for DevToolKit v1.0.0 — 16 tools, zero dependencies, pure Python.*
