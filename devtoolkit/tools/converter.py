"""
Format Converter — Convert between JSON and CSV formats.

Usage:
    python -m devtoolkit convert <input_file> [--output FILE] [--pretty]
"""

import argparse
import csv
import io
import json
from pathlib import Path


def json_to_csv(data: list[dict], output_path: str | None = None) -> str:
    """Convert a list of JSON objects to CSV."""
    if not data:
        return ""

    # Collect all unique keys across all objects
    fieldnames = []
    seen = set()
    for row in data:
        for key in row.keys():
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in data:
        # Flatten nested objects to JSON strings
        flat = {}
        for k, v in row.items():
            if isinstance(v, (dict, list)):
                flat[k] = json.dumps(v)
            else:
                flat[k] = v
        writer.writerow(flat)

    result = output.getvalue()

    if output_path:
        Path(output_path).write_text(result, encoding="utf-8")
        print(f"  Saved CSV to: {output_path}")

    return result


def csv_to_json(csv_text: str, output_path: str | None = None, pretty: bool = True) -> list[dict]:
    """Convert CSV text to a list of JSON objects."""
    reader = csv.DictReader(io.StringIO(csv_text))
    data = []
    for row in reader:
        clean_row = {}
        for k, v in row.items():
            # Try to parse JSON strings back into objects
            try:
                clean_row[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                # Try to convert numbers
                try:
                    if "." in v:
                        clean_row[k] = float(v)
                    else:
                        clean_row[k] = int(v)
                except (ValueError, TypeError):
                    clean_row[k] = v
        data.append(clean_row)

    if output_path:
        indent = 2 if pretty else None
        Path(output_path).write_text(
            json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  Saved JSON to: {output_path}")

    return data


def detect_and_convert(input_path: str, output_path: str | None, pretty: bool) -> int:
    """Auto-detect format and convert."""
    path = Path(input_path)
    if not path.exists():
        print(f"  Error: File '{input_path}' not found.")
        return 1

    content = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()

    if ext == ".json":
        # JSON -> CSV
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON: {e}")
            return 1

        if isinstance(data, dict):
            # Attempt to find an array in the top-level keys
            for key, val in data.items():
                if isinstance(val, list) and val and isinstance(val[0], dict):
                    data = val
                    print(f"  Using array from key '{key}' ({len(data)} records)")
                    break
            else:
                data = [data]

        if not isinstance(data, list):
            print("  Error: JSON must be an array of objects (or contain one).")
            return 1

        out = output_path or str(path.with_suffix(".csv"))
        result = json_to_csv(data, out)
        lines = result.strip().count("\n")
        print(f"  Converted {len(data)} records to CSV ({lines + 1} lines).")

    elif ext == ".csv":
        # CSV -> JSON
        out = output_path or str(path.with_suffix(".json"))
        data = csv_to_json(content, out, pretty)
        print(f"  Converted {len(data)} records to JSON.")

    else:
        # Try to auto-detect
        content_stripped = content.strip()
        if content_stripped.startswith(("{", "[")):
            print("  Detected JSON input.")
            data = json.loads(content)
            if not isinstance(data, list):
                data = [data]
            out = output_path or str(path.with_suffix(".csv"))
            json_to_csv(data, out)
        else:
            print("  Detected CSV input.")
            out = output_path or str(path.with_suffix(".json"))
            csv_to_json(content, out, pretty)

    return 0


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit convert",
        description="Convert between JSON and CSV formats.",
    )
    parser.add_argument("input", help="Input file (JSON or CSV)")
    parser.add_argument("-o", "--output", help="Output file path (auto-detected if omitted)")
    parser.add_argument("--pretty", action="store_true", default=True,
                        help="Pretty-print JSON output (default: True)")
    parser.add_argument("--compact", action="store_false", dest="pretty",
                        help="Compact JSON output")
    args = parser.parse_args(argv)

    print()
    result = detect_and_convert(args.input, args.output, args.pretty)
    print()
    return result
