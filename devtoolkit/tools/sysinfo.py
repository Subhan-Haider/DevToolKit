"""
System Info — Display detailed system and environment information.

Usage:
    python -m devtoolkit sysinfo [--json]
"""

import argparse
import json
import os
import platform
import shutil
import socket
import sys
from datetime import datetime


def get_disk_usage(path: str = "/") -> dict:
    """Get disk usage for a path."""
    try:
        if platform.system() == "Windows":
            path = os.environ.get("SystemDrive", "C:\\")
        usage = shutil.disk_usage(path)
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent_used": round(usage.used / usage.total * 100, 1),
        }
    except Exception:
        return {"error": "Could not read disk usage"}


def get_network_info() -> dict:
    """Get basic network information."""
    info = {"hostname": socket.gethostname()}
    try:
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        info["ip_address"] = "Unknown"
    try:
        info["fqdn"] = socket.getfqdn()
    except Exception:
        info["fqdn"] = "Unknown"
    return info


def get_python_info() -> dict:
    """Get Python environment details."""
    return {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "compiler": platform.python_compiler(),
        "executable": sys.executable,
        "prefix": sys.prefix,
        "path": sys.path[:5],
    }


def get_env_tools() -> dict:
    """Check for common dev tools."""
    tools = {}
    tool_commands = {
        "git": "git --version",
        "node": "node --version",
        "npm": "npm --version",
        "python3": "python3 --version",
        "docker": "docker --version",
        "cargo": "cargo --version",
        "go": "go version",
        "java": "java -version",
    }
    for name, cmd in tool_commands.items():
        path = shutil.which(name)
        tools[name] = "installed" if path else "not found"
    return tools


def collect_info() -> dict:
    """Collect all system information."""
    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor() or "Unknown",
            "platform": platform.platform(),
        },
        "python": get_python_info(),
        "network": get_network_info(),
        "disk": get_disk_usage(),
        "dev_tools": get_env_tools(),
        "environment": {
            "user": os.environ.get("USERNAME") or os.environ.get("USER", "Unknown"),
            "home": str(os.path.expanduser("~")),
            "cwd": os.getcwd(),
            "shell": os.environ.get("SHELL") or os.environ.get("COMSPEC", "Unknown"),
            "terminal": os.environ.get("TERM", os.environ.get("WT_SESSION", "Unknown")),
            "path_entries": len(os.environ.get("PATH", "").split(os.pathsep)),
        },
    }


def print_info(info: dict) -> None:
    """Pretty-print system information."""
    def section(title: str) -> None:
        print(f"\n  {'=' * 55}")
        print(f"  {title}")
        print(f"  {'=' * 55}")

    def row(key: str, value) -> None:
        print(f"    {key:<22} {value}")

    section("SYSTEM")
    for k, v in info["system"].items():
        row(k.replace("_", " ").title(), v)

    section("PYTHON")
    for k, v in info["python"].items():
        if k == "path":
            row("Sys.path (first 5)", "")
            for p in v:
                print(f"      {p}")
        else:
            row(k.replace("_", " ").title(), v)

    section("NETWORK")
    for k, v in info["network"].items():
        row(k.replace("_", " ").title(), v)

    section("DISK")
    disk = info["disk"]
    if "error" not in disk:
        row("Total", f"{disk['total_gb']} GB")
        row("Used", f"{disk['used_gb']} GB ({disk['percent_used']}%)")
        row("Free", f"{disk['free_gb']} GB")
        # Visual bar
        filled = int(disk["percent_used"] / 2)
        bar = "█" * filled + "░" * (50 - filled)
        print(f"    [{bar}]")

    section("DEV TOOLS")
    for tool, status in info["dev_tools"].items():
        icon = "✓" if status == "installed" else "✗"
        row(f"{icon} {tool}", status)

    section("ENVIRONMENT")
    for k, v in info["environment"].items():
        row(k.replace("_", " ").title(), v)
    print()


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit sysinfo",
        description="Display detailed system information.",
    )
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    args = parser.parse_args(argv)

    info = collect_info()

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print_info(info)

    return 0
