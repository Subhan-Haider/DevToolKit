"""
Password Generator — Generate strong, customizable passwords and passphrases.

Usage:
    python -m devtoolkit password [--length N] [--count N] [--no-symbols]
                                  [--passphrase] [--words N] [--copy]
"""

import argparse
import secrets
import string


# Common English words for passphrases (curated for memorability)
WORDLIST = [
    "anchor", "breeze", "castle", "dragon", "ember", "falcon", "glacier",
    "harbor", "island", "jungle", "knight", "lantern", "meadow", "nectar",
    "oracle", "phoenix", "quartz", "ripple", "summit", "timber", "umbra",
    "violet", "whisper", "zenith", "aurora", "beacon", "canyon", "dawn",
    "eclipse", "forest", "garden", "horizon", "ivory", "jasper", "kindle",
    "lunar", "marble", "nebula", "oasis", "prism", "quest", "river",
    "silver", "thunder", "unity", "voyage", "willow", "crystal", "spark",
    "storm", "coral", "velvet", "lotus", "raven", "atlas", "blaze",
    "cedar", "drift", "echo", "flame", "glow", "haze", "iris",
    "jewel", "kelp", "lace", "mist", "nova", "onyx", "pearl",
    "rain", "sage", "tide", "vale", "wave", "amber", "bloom",
    "crest", "dusk", "fern", "grace", "honey", "jade", "lake",
    "moon", "north", "ocean", "pine", "reef", "snow", "trail",
    "vine", "wing", "aura", "bell", "cliff", "delta", "frost",
]


def generate_password(length: int = 20, use_symbols: bool = True) -> str:
    """Generate a cryptographically secure random password."""
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    # Ensure at least one of each required type
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    if use_symbols:
        password.append(secrets.choice("!@#$%^&*()-_=+[]{}|;:,.<>?"))

    remaining = length - len(password)
    password.extend(secrets.choice(chars) for _ in range(remaining))

    # Shuffle to avoid predictable positions
    result = list(password)
    secrets.SystemRandom().shuffle(result)
    return "".join(result)


def generate_passphrase(num_words: int = 5, separator: str = "-") -> str:
    """Generate a memorable passphrase from random words."""
    words = [secrets.choice(WORDLIST) for _ in range(num_words)]
    # Capitalize one random word and add a random digit
    cap_index = secrets.randbelow(num_words)
    words[cap_index] = words[cap_index].capitalize()
    digit = str(secrets.randbelow(100))
    words.insert(secrets.randbelow(len(words) + 1), digit)
    return separator.join(words)


def password_strength(password: str) -> str:
    """Estimate password strength."""
    score = 0
    if len(password) >= 8:  score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 20: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    levels = {0: "Very Weak", 1: "Very Weak", 2: "Weak", 3: "Weak",
              4: "Fair", 5: "Strong", 6: "Very Strong", 7: "Excellent"}
    return levels.get(score, "Excellent")


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit password",
        description="Generate strong passwords and passphrases.",
    )
    parser.add_argument("-l", "--length", type=int, default=20,
                        help="Password length (default: 20)")
    parser.add_argument("-c", "--count", type=int, default=5,
                        help="Number of passwords to generate (default: 5)")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude special characters")
    parser.add_argument("--passphrase", action="store_true",
                        help="Generate passphrases instead of passwords")
    parser.add_argument("-w", "--words", type=int, default=5,
                        help="Number of words in passphrase (default: 5)")
    parser.add_argument("--copy", action="store_true",
                        help="Copy the first password to clipboard")
    args = parser.parse_args(argv)

    print()
    if args.passphrase:
        print("  Generated Passphrases:")
        print("  " + "-" * 50)
        results = []
        for i in range(args.count):
            pp = generate_passphrase(num_words=args.words)
            results.append(pp)
            strength = password_strength(pp)
            print(f"  {i+1}. {pp}")
            print(f"     Strength: {strength} | Length: {len(pp)} chars")
    else:
        print("  Generated Passwords:")
        print("  " + "-" * 50)
        results = []
        for i in range(args.count):
            pw = generate_password(length=args.length, use_symbols=not args.no_symbols)
            results.append(pw)
            strength = password_strength(pw)
            print(f"  {i+1}. {pw}")
            print(f"     Strength: {strength} | Length: {len(pw)} chars")

    if args.copy:
        try:
            import subprocess
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            process.communicate(results[0].encode())
            print(f"\n  First password copied to clipboard!")
        except Exception:
            print(f"\n  Could not copy to clipboard (install xclip/xsel on Linux).")

    print()
    return 0
