"""
Quick HTTP Server — Serve files from a directory with a nice listing page.

Usage:
    python -m devtoolkit serve [DIRECTORY] [--port PORT] [--open]
"""

import argparse
import html
import os
import socket
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial


class DevToolKitHandler(SimpleHTTPRequestHandler):
    """Enhanced HTTP handler with a styled directory listing."""

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"  {self.address_string()} - {format % args}")

    def list_directory(self, path):
        """Generate a styled directory listing."""
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(403, "Permission denied")
            return None

        entries.sort(key=lambda e: (not os.path.isdir(os.path.join(path, e)), e.lower()))

        rel_path = os.path.relpath(path, self.directory)
        if rel_path == ".":
            title = "/"
        else:
            title = "/" + rel_path.replace("\\", "/")

        items_html = ""
        if title != "/":
            items_html += '<tr><td>📁</td><td><a href="..">..</a></td><td>—</td><td>—</td></tr>\n'

        for name in entries:
            if name.startswith("."):
                continue
            fullpath = os.path.join(path, name)
            is_dir = os.path.isdir(fullpath)
            display = html.escape(name)
            link = html.escape(name) + ("/" if is_dir else "")
            icon = "📁" if is_dir else "📄"

            try:
                stat = os.stat(fullpath)
                size = "—" if is_dir else format_size(stat.st_size)
                from datetime import datetime
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            except OSError:
                size = "?"
                mtime = "?"

            items_html += f'<tr><td>{icon}</td><td><a href="{link}">{display}</a></td><td>{size}</td><td>{mtime}</td></tr>\n'

        page = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DevToolKit — {html.escape(title)}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #1a1b26; color: #c0caf5; padding: 2rem; }}
  h1 {{ color: #7aa2f7; margin-bottom: 0.5rem; font-size: 1.4rem; }}
  .subtitle {{ color: #565f89; margin-bottom: 1.5rem; font-size: 0.85rem; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; color: #565f89; border-bottom: 1px solid #292e42;
       padding: 0.5rem; font-size: 0.8rem; text-transform: uppercase; }}
  td {{ padding: 0.6rem 0.5rem; border-bottom: 1px solid #292e42; }}
  a {{ color: #7dcfff; text-decoration: none; }}
  a:hover {{ color: #bb9af7; text-decoration: underline; }}
  tr:hover {{ background: #292e42; }}
  .footer {{ color: #565f89; margin-top: 2rem; font-size: 0.75rem; text-align: center; }}
</style></head><body>
<h1>📂 {html.escape(title)}</h1>
<p class="subtitle">DevToolKit File Server</p>
<table>
<tr><th></th><th>Name</th><th>Size</th><th>Modified</th></tr>
{items_html}
</table>
<p class="footer">DevToolKit v1.0 — Ctrl+C to stop</p>
</body></html>"""

        encoded = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        from io import BytesIO
        return BytesIO(encoded)


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit serve",
        description="Quick HTTP file server with styled directory listing.",
    )
    parser.add_argument("directory", nargs="?", default=".",
                        help="Directory to serve (default: current dir)")
    parser.add_argument("-p", "--port", type=int, default=8000,
                        help="Port to listen on (default: 8000)")
    parser.add_argument("--open", action="store_true",
                        help="Open browser automatically")
    parser.add_argument("--bind", default="0.0.0.0",
                        help="Address to bind to (default: 0.0.0.0)")
    args = parser.parse_args(argv)

    directory = str(Path(args.directory).resolve())
    handler = partial(DevToolKitHandler, directory=directory)

    try:
        server = HTTPServer((args.bind, args.port), handler)
    except OSError as e:
        if "address already in use" in str(e).lower() or "10048" in str(e):
            print(f"\n  Error: Port {args.port} is already in use. Try --port {args.port + 1}")
            return 1
        raise

    local_ip = get_local_ip()
    print(f"\n  DevToolKit File Server")
    print(f"  {'─' * 45}")
    print(f"  Serving:   {directory}")
    print(f"  Local:     http://localhost:{args.port}")
    print(f"  Network:   http://{local_ip}:{args.port}")
    print(f"  {'─' * 45}")
    print(f"  Press Ctrl+C to stop.\n")

    if args.open:
        threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{args.port}")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()

    return 0
