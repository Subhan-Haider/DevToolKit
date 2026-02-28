"""
Lorem Ipsum Generator — Generate placeholder text for designs and mockups.

Usage:
    python -m devtoolkit lorem [--paragraphs N] [--words N] [--sentences N]
                               [--format FORMAT] [--copy]
"""

import argparse
import random
import textwrap

# Classic Lorem Ipsum vocabulary
WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
    "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
    "et", "dolore", "magna", "aliqua", "enim", "ad", "minim", "veniam",
    "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi",
    "aliquip", "ex", "ea", "commodo", "consequat", "duis", "aute", "irure",
    "in", "reprehenderit", "voluptate", "velit", "esse", "cillum", "fugiat",
    "nulla", "pariatur", "excepteur", "sint", "occaecat", "cupidatat",
    "non", "proident", "sunt", "culpa", "qui", "officia", "deserunt",
    "mollit", "anim", "id", "est", "laborum", "ac", "accumsan", "aliquet",
    "ante", "arcu", "at", "augue", "bibendum", "blandit", "commodo",
    "condimentum", "congue", "consequat", "convallis", "cras", "curabitur",
    "cursus", "dapibus", "diam", "dictum", "dignissim", "donec",
    "efficitur", "elementum", "erat", "eros", "etiam", "euismod",
    "facilisis", "fames", "faucibus", "felis", "fermentum", "feugiat",
    "finibus", "fringilla", "fusce", "gravida", "habitant", "hendrerit",
    "iaculis", "imperdiet", "integer", "interdum", "justo", "lacinia",
    "lacus", "laoreet", "lectus", "leo", "libero", "ligula", "lobortis",
    "luctus", "maecenas", "massa", "mattis", "mauris", "maximus",
    "metus", "mi", "morbi", "nam", "nec", "neque", "nibh", "nisl",
    "nullam", "nunc", "odio", "orci", "ornare", "pellentesque",
    "pharetra", "placerat", "porta", "posuere", "praesent", "pretium",
    "primis", "proin", "pulvinar", "purus", "quam", "quisque",
    "rhoncus", "risus", "rutrum", "sagittis", "sapien", "scelerisque",
    "semper", "senectus", "sociosqu", "sodales", "sollicitudin",
    "suscipit", "suspendisse", "tellus", "tincidunt", "tortor",
    "tristique", "turpis", "ultrices", "ultricies", "urna", "varius",
    "vehicula", "vel", "vestibulum", "vitae", "vivamus", "viverra",
    "volutpat", "vulputate",
]

FIRST_SENTENCE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


def generate_sentence(min_words: int = 6, max_words: int = 15) -> str:
    length = random.randint(min_words, max_words)
    words = [random.choice(WORDS) for _ in range(length)]
    words[0] = words[0].capitalize()

    # Sometimes add a comma
    if length > 8:
        comma_pos = random.randint(3, length - 3)
        words[comma_pos] += ","

    return " ".join(words) + "."


def generate_paragraph(num_sentences: int = 0) -> str:
    if num_sentences <= 0:
        num_sentences = random.randint(4, 8)
    return " ".join(generate_sentence() for _ in range(num_sentences))


def generate_words(count: int) -> str:
    return " ".join(random.choice(WORDS) for _ in range(count))


def format_output(text: str, fmt: str) -> str:
    """Format output for different use cases."""
    if fmt == "html":
        paragraphs = text.split("\n\n")
        return "\n".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    elif fmt == "markdown":
        return text
    elif fmt == "json":
        import json
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        return json.dumps({"paragraphs": paragraphs, "full_text": text.strip()}, indent=2)
    elif fmt == "wrapped":
        paragraphs = text.split("\n\n")
        wrapped = []
        for p in paragraphs:
            if p.strip():
                wrapped.append(textwrap.fill(p.strip(), width=72))
        return "\n\n".join(wrapped)
    return text


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit lorem",
        description="Generate placeholder text (Lorem Ipsum).",
    )
    parser.add_argument("-p", "--paragraphs", type=int, default=3,
                        help="Number of paragraphs (default: 3)")
    parser.add_argument("-w", "--words", type=int,
                        help="Generate exactly N words instead of paragraphs")
    parser.add_argument("-s", "--sentences", type=int,
                        help="Sentences per paragraph")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "html", "markdown", "json", "wrapped"],
                        help="Output format (default: text)")
    parser.add_argument("--no-lorem", action="store_true",
                        help="Don't start with 'Lorem ipsum dolor sit amet'")
    parser.add_argument("--copy", action="store_true",
                        help="Copy to clipboard")
    parser.add_argument("-o", "--output", help="Save to file")
    args = parser.parse_args(argv)

    print()

    if args.words:
        text = generate_words(args.words)
        if not args.no_lorem and args.words >= 5:
            text = "Lorem ipsum dolor sit amet " + text
            # Trim to exact word count
            text = " ".join(text.split()[:args.words])
    else:
        paragraphs = []
        for i in range(args.paragraphs):
            para = generate_paragraph(args.sentences or 0)
            if i == 0 and not args.no_lorem:
                # Start with the classic opening
                rest = generate_paragraph(max(0, (args.sentences or 5) - 1))
                para = FIRST_SENTENCE + " " + rest
            paragraphs.append(para)
        text = "\n\n".join(paragraphs)

    formatted = format_output(text, args.format)
    print(formatted)

    word_count = len(text.split())
    char_count = len(text)

    if args.output:
        Path(args.output).write_text(formatted, encoding="utf-8")
        print(f"\n  Saved to: {args.output}")

    if args.copy:
        try:
            import subprocess
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            process.communicate(formatted.encode())
            print(f"\n  Copied to clipboard!")
        except Exception:
            pass

    print(f"\n  Generated: {word_count} words, {char_count} characters\n")
    return 0
