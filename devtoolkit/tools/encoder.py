"""
Encoder/Decoder — Base64, URL, HTML encode/decode and more.

Usage:
    python -m devtoolkit encode <format> <text_or_file>
    python -m devtoolkit encode base64 "Hello World"
    python -m devtoolkit encode url "hello world & more"
    python -m devtoolkit encode base64 --decode "SGVsbG8gV29ybGQ="
    python -m devtoolkit encode jwt "eyJhbGciOiJI..." --decode
"""

import argparse
import base64
import html as html_module
import json
import urllib.parse
from pathlib import Path


FORMATS = {
    "base64":  "Base64 encode/decode",
    "url":     "URL (percent) encode/decode",
    "html":    "HTML entity encode/decode",
    "hex":     "Hexadecimal encode/decode",
    "binary":  "Binary (0s and 1s) representation",
    "rot13":   "ROT13 cipher",
    "jwt":     "Decode JWT tokens (no verification)",
    "unicode": "Unicode escape/unescape",
}


def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_base64(text: str) -> str:
    # Handle URL-safe base64 and missing padding
    text = text.strip()
    text += "=" * (4 - len(text) % 4) if len(text) % 4 else ""
    try:
        return base64.b64decode(text).decode("utf-8")
    except Exception:
        return base64.urlsafe_b64decode(text).decode("utf-8")


def encode_url(text: str) -> str:
    return urllib.parse.quote(text, safe="")


def decode_url(text: str) -> str:
    return urllib.parse.unquote(text)


def encode_html(text: str) -> str:
    return html_module.escape(text)


def decode_html(text: str) -> str:
    return html_module.unescape(text)


def encode_hex(text: str) -> str:
    return text.encode("utf-8").hex()


def decode_hex(text: str) -> str:
    return bytes.fromhex(text.strip()).decode("utf-8")


def encode_binary(text: str) -> str:
    return " ".join(f"{b:08b}" for b in text.encode("utf-8"))


def decode_binary(text: str) -> str:
    bits = text.replace(" ", "")
    bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list).decode("utf-8")


def encode_rot13(text: str) -> str:
    import codecs
    return codecs.encode(text, "rot_13")


def decode_rot13(text: str) -> str:
    return encode_rot13(text)  # ROT13 is its own inverse


def decode_jwt(token: str) -> str:
    """Decode a JWT token without verification."""
    parts = token.strip().split(".")
    if len(parts) < 2:
        return "Error: Not a valid JWT token (expected 2-3 parts separated by dots)"

    result = []
    labels = ["Header", "Payload", "Signature"]
    for i, part in enumerate(parts[:2]):
        # Fix base64url padding
        padded = part + "=" * (4 - len(part) % 4)
        try:
            decoded = base64.urlsafe_b64decode(padded).decode("utf-8")
            parsed = json.loads(decoded)
            result.append(f"  {labels[i]}:")
            result.append(f"  {json.dumps(parsed, indent=4)}")
        except Exception as e:
            result.append(f"  {labels[i]}: (decode error: {e})")

    if len(parts) == 3:
        result.append(f"  {labels[2]}: {parts[2][:50]}...")

    return "\n".join(result)


def encode_unicode(text: str) -> str:
    return text.encode("unicode_escape").decode("ascii")


def decode_unicode(text: str) -> str:
    return text.encode("ascii").decode("unicode_escape")


ENCODERS = {
    "base64": (encode_base64, decode_base64),
    "url": (encode_url, decode_url),
    "html": (encode_html, decode_html),
    "hex": (encode_hex, decode_hex),
    "binary": (encode_binary, decode_binary),
    "rot13": (encode_rot13, decode_rot13),
    "jwt": (None, decode_jwt),
    "unicode": (encode_unicode, decode_unicode),
}


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit encode",
        description="Encode and decode text in various formats.",
    )
    parser.add_argument("format", nargs="?", choices=list(FORMATS.keys()),
                        help="Encoding format")
    parser.add_argument("text", nargs="?", help="Text to encode/decode (or file path)")
    parser.add_argument("-d", "--decode", action="store_true",
                        help="Decode instead of encode")
    parser.add_argument("-f", "--file", action="store_true",
                        help="Treat input as a file path")
    parser.add_argument("--list", action="store_true",
                        help="List available formats")
    args = parser.parse_args(argv)

    print()

    if args.list or not args.format:
        print(f"  Available Formats:")
        print(f"  {'─' * 45}")
        for fmt, desc in FORMATS.items():
            print(f"    {fmt:<10}  {desc}")
        print(f"\n  Usage: devtoolkit encode <format> <text>")
        print(f"         devtoolkit encode <format> <text> --decode\n")
        return 0

    if not args.text:
        print("  Error: No input text provided.")
        return 1

    text = args.text
    if args.file:
        path = Path(text)
        if not path.is_file():
            print(f"  Error: File '{text}' not found.")
            return 1
        text = path.read_text(encoding="utf-8")

    encoder, decoder = ENCODERS[args.format]
    action = "Decode" if args.decode else "Encode"

    try:
        if args.decode:
            if args.format == "jwt":
                result = decoder(text)
                print(f"  JWT Token Decoded:")
                print(f"  {'─' * 45}")
                print(result)
            else:
                result = decoder(text)
                print(f"  {action}d ({args.format}):")
                print(f"  {'─' * 45}")
                print(f"  {result}")
        else:
            if encoder is None:
                print(f"  '{args.format}' format only supports decoding.")
                return 1
            result = encoder(text)
            print(f"  {action}d ({args.format}):")
            print(f"  {'─' * 45}")
            print(f"  {result}")

        print(f"  {'─' * 45}")
        input_len = len(text)
        output_len = len(result) if isinstance(result, str) else 0
        print(f"  Input: {input_len} chars → Output: {output_len} chars")

    except Exception as e:
        print(f"  Error: {e}")
        return 1

    print()
    return 0
