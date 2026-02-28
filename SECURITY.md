# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in DevToolKit, please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. Email: Send details to your preferred security contact email
3. Or use [GitHub Security Advisories](https://github.com/YOUR_USERNAME/devtoolkit/security/advisories/new) (private)

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Which tool is affected (e.g., `serve`, `encode`, `hash`)
- Potential impact
- Suggested fix (if any)

### Response Timeline

| Action | Timeframe |
|--------|-----------|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 1 week |
| Fix released | Within 2 weeks (critical) / 30 days (moderate) |

## Security Considerations by Tool

### `serve` — HTTP Server
- **Not for production.** Uses Python's built-in `http.server`, which is not hardened.
- Only use on trusted local networks (LAN).
- Do not expose to the public internet.
- Does not support HTTPS/TLS.
- Binds to `0.0.0.0` by default — use `--bind 127.0.0.1` to restrict to localhost only.

### `password` — Password Generator
- Uses `secrets` module (cryptographically secure PRNG).
- Generated passwords are only printed to stdout — they are **not** logged or stored anywhere.
- `--copy` uses the system clipboard which other apps can read — clear it after use.

### `hash` — Hash Calculator
- Uses Python's `hashlib` (OpenSSL-backed).
- MD5 and SHA1 are provided for compatibility/verification only — **do not use for security purposes**. Use SHA256+ for integrity checks.

### `encode` — Encoder/Decoder
- JWT decode (`--decode`) **does not verify signatures**. It only decodes the payload for inspection.
- Do not use this for authentication or security decisions.
- ROT13 is a toy cipher — it provides **zero security**.

### `snippet` / `todo` — Data Storage
- Data stored as plain-text JSON in your home directory (`~/.devtoolkit_*.json`).
- **Do not store secrets, passwords, or API keys** in snippets or todos.
- Anyone with access to your home directory can read these files.

### `organize` — File Organizer
- Moves files on disk. Always use `--dry-run` first to preview changes.
- Undo log (`_organize_log.json`) is stored in the organized directory.

### `search` — Text Search
- Skips binary files and common excluded directories (`.git`, `node_modules`, etc.).
- File contents are read into memory — avoid using on very large files (>100MB).

### `convert` — JSON/CSV Converter
- Reads entire files into memory. Not suitable for multi-GB datasets.

### `diff` — File Diff
- `--html` output generates a local HTML file. Do not serve it publicly if it contains sensitive data.

## General Security Notes

- **Zero dependencies** — no supply-chain risk from third-party packages.
- **No network calls** — except `serve` (local HTTP server) and `sysinfo` (local IP detection via UDP socket, no data sent).
- **No telemetry** — nothing is collected, reported, or sent anywhere.
- **No eval/exec** — user input is never executed as code.
- **Regex patterns** (`search`, `regex`) are compiled with `re.compile()` — malicious ReDoS patterns could cause slowdowns but not code execution.

## Best Practices

1. Keep Python updated (3.10+) for the latest security patches
2. Don't run `serve` on untrusted networks
3. Don't store secrets in `snippet` or `todo`
4. Use `--dry-run` before `organize` on important directories
5. Verify file hashes with SHA256 (`--algo sha256`), not MD5
6. Review the source — it's ~2000 lines of readable Python, easy to audit
