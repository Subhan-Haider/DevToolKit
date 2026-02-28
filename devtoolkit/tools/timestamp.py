"""
Timestamp Converter — Convert between Unix timestamps, ISO dates, and human-readable formats.

Usage:
    python -m devtoolkit timestamp                  # Show current time in all formats
    python -m devtoolkit timestamp 1709078400        # Unix -> readable
    python -m devtoolkit timestamp "2024-02-28"      # Date -> Unix
    python -m devtoolkit timestamp --diff "2024-01-01" "2025-01-01"
"""

import argparse
import time
from datetime import datetime, timezone, timedelta


def now_info() -> dict:
    """Get current time in multiple formats."""
    now = datetime.now()
    utc_now = datetime.now(timezone.utc)
    return {
        "unix": int(now.timestamp()),
        "unix_ms": int(now.timestamp() * 1000),
        "iso_local": now.isoformat(),
        "iso_utc": utc_now.isoformat(),
        "human": now.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "utc_offset": now.astimezone().strftime("%z"),
        "week_number": now.isocalendar()[1],
        "day_of_year": now.timetuple().tm_yday,
    }


def parse_input(value: str) -> datetime:
    """Try to parse a timestamp or date string."""
    # Try Unix timestamp (seconds)
    try:
        ts = float(value)
        if ts > 1e12:  # Likely milliseconds
            ts /= 1000
        return datetime.fromtimestamp(ts)
    except (ValueError, OverflowError, OSError):
        pass

    # Try common date formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError(f"Could not parse: '{value}'")


def format_delta(td: timedelta) -> str:
    """Human-readable timedelta."""
    total_seconds = int(abs(td.total_seconds()))
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if days > 365:
        years = days // 365
        days %= 365
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if days > 30:
        months = days // 30
        days %= 30
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit timestamp",
        description="Convert between timestamps and date formats.",
    )
    parser.add_argument("value", nargs="?",
                        help="Unix timestamp, ISO date, or date string (omit for current time)")
    parser.add_argument("--diff", nargs=2, metavar=("FROM", "TO"),
                        help="Calculate difference between two dates/timestamps")
    parser.add_argument("--add", metavar="DURATION",
                        help="Add duration to value (e.g., '7d', '3h', '30m', '2w')")
    args = parser.parse_args(argv)

    print()

    if args.diff:
        try:
            dt1 = parse_input(args.diff[0])
            dt2 = parse_input(args.diff[1])
        except ValueError as e:
            print(f"  Error: {e}")
            return 1

        delta = dt2 - dt1
        print(f"  From:       {dt1.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  To:         {dt2.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {'─' * 50}")
        print(f"  Difference: {format_delta(delta)}")
        print(f"  Days:       {abs(delta.days):,}")
        print(f"  Hours:      {int(abs(delta.total_seconds()) // 3600):,}")
        print(f"  Minutes:    {int(abs(delta.total_seconds()) // 60):,}")
        print(f"  Seconds:    {int(abs(delta.total_seconds())):,}")
        print()
        return 0

    if args.value:
        try:
            dt = parse_input(args.value)
        except ValueError as e:
            print(f"  Error: {e}")
            return 1
        print(f"  Input:      {args.value}")
    else:
        dt = datetime.now()
        print(f"  Current Time")

    if args.add:
        duration = args.add.strip()
        multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        unit = duration[-1].lower()
        if unit in multiplier:
            try:
                amount = float(duration[:-1])
                dt = dt + timedelta(seconds=amount * multiplier[unit])
                print(f"  Added:      {args.add}")
            except ValueError:
                print(f"  Error: Invalid duration '{args.add}'")
                return 1
        else:
            print(f"  Error: Unknown unit '{unit}'. Use s/m/h/d/w.")
            return 1

    delta_from_now = datetime.now() - dt
    relative = format_delta(delta_from_now)
    direction = "ago" if delta_from_now.total_seconds() > 0 else "from now"

    print(f"  {'─' * 50}")
    print(f"  Unix:       {int(dt.timestamp())}")
    print(f"  Unix (ms):  {int(dt.timestamp() * 1000)}")
    print(f"  ISO 8601:   {dt.isoformat()}")
    print(f"  Human:      {dt.strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
    print(f"  Date:       {dt.strftime('%Y-%m-%d')}")
    print(f"  Time:       {dt.strftime('%H:%M:%S')}")
    print(f"  Relative:   {relative} {direction}")
    print(f"  Week #:     {dt.isocalendar()[1]}")
    print(f"  Day of year: {dt.timetuple().tm_yday}")
    print()
    return 0
