"""AI assistant powered by Ollama (local LLM).

Connects to Ollama's local REST API at http://localhost:11434.
Requires Ollama to be installed and running: https://ollama.com

Features:
  - Chat with any local model (interactive or single prompt)
  - Summarise files
  - Explain / review code
  - Generate code from a description
  - List & pull models

Zero external dependencies — uses only urllib from the standard library.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import textwrap

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# ── helpers ──────────────────────────────────────────────────────────

def _api(path, payload=None, stream=False):
    """Call the Ollama REST API. Returns parsed JSON or a generator for streams."""
    url = f"{OLLAMA_HOST}{path}"
    headers = {"Content-Type": "application/json"}

    if payload is not None:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        resp = urllib.request.urlopen(req, timeout=300)
    except urllib.error.URLError as exc:
        print(f"\n  Error: Cannot connect to Ollama at {OLLAMA_HOST}")
        print(f"  Detail: {exc.reason}\n")
        print("  Make sure Ollama is installed and running:")
        print("    1. Install: https://ollama.com/download")
        print("    2. Start:   ollama serve")
        print("    3. Pull a model: ollama pull llama3\n")
        sys.exit(1)

    if stream:
        return _stream_response(resp)
    else:
        return json.loads(resp.read().decode())


def _stream_response(resp):
    """Yield parsed JSON objects from a streaming (NDJSON) response."""
    buffer = b""
    while True:
        chunk = resp.read(4096)
        if not chunk:
            break
        buffer += chunk
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            line = line.strip()
            if line:
                yield json.loads(line)


def _stream_print(gen):
    """Print streamed tokens and return the full response text."""
    full = []
    for obj in gen:
        # /api/generate format
        token = obj.get("response", "")
        # /api/chat format
        if not token:
            msg = obj.get("message", {})
            token = msg.get("content", "")
        if token:
            print(token, end="", flush=True)
            full.append(token)
        if obj.get("done"):
            break
    print()  # newline after stream
    return "".join(full)


# ── commands ─────────────────────────────────────────────────────────

def cmd_models(_args):
    """List locally available Ollama models."""
    data = _api("/api/tags")
    models = data.get("models", [])
    if not models:
        print("\n  No models found. Pull one first:")
        print("    ollama pull llama3\n")
        return

    print(f"\n  {'Model':<30} {'Size':<12} {'Modified'}")
    print(f"  {'─'*30} {'─'*12} {'─'*20}")
    for m in models:
        name = m.get("name", "?")
        size_bytes = m.get("size", 0)
        size_gb = size_bytes / (1024**3)
        if size_gb >= 1:
            size_str = f"{size_gb:.1f} GB"
        else:
            size_str = f"{size_bytes / (1024**2):.0f} MB"
        modified = m.get("modified_at", "?")[:19].replace("T", " ")
        print(f"  {name:<30} {size_str:<12} {modified}")
    print()


def cmd_pull(args):
    """Pull / download a model."""
    model = args.model_name
    print(f"\n  Pulling model '{model}' ... (this may take a while)\n")

    payload = {"name": model, "stream": True}
    gen = _api("/api/pull", payload, stream=True)

    last_status = ""
    for obj in gen:
        status = obj.get("status", "")
        if status != last_status:
            print(f"  {status}")
            last_status = status

    print(f"\n  Done! Model '{model}' is ready.")
    print(f"  Use:  python -m devtoolkit ai chat --model {model}\n")


def cmd_chat(args):
    """Interactive chat or single-prompt mode."""
    model = args.model
    system_prompt = args.system or ""

    # ── single prompt mode ──
    if args.prompt:
        prompt_text = " ".join(args.prompt)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt_text})

        print(f"\n  Model: {model}")
        print(f"  {'─'*50}\n")

        payload = {"model": model, "messages": messages, "stream": True}
        _stream_print(_api("/api/chat", payload, stream=True))
        print()
        return

    # ── interactive mode ──
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    print(f"\n  ╔══════════════════════════════════════╗")
    print(f"  ║  DevToolKit AI Chat — {model:<15}║")
    print(f"  ╠══════════════════════════════════════╣")
    print(f"  ║  Type your message and press Enter.  ║")
    print(f"  ║  Commands: /quit  /clear  /model      ║")
    print(f"  ╚══════════════════════════════════════╝\n")

    while True:
        try:
            user_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye!\n")
            break

        if not user_input:
            continue
        if user_input.lower() in ("/quit", "/exit", "/q"):
            print("\n  Goodbye!\n")
            break
        if user_input.lower() == "/clear":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            print("  (conversation cleared)\n")
            continue
        if user_input.lower() == "/model":
            cmd_models(None)
            continue

        messages.append({"role": "user", "content": user_input})
        payload = {"model": model, "messages": messages, "stream": True}

        print(f"\n  AI: ", end="", flush=True)
        reply = _stream_print(_api("/api/chat", payload, stream=True))
        print()

        messages.append({"role": "assistant", "content": reply})


def cmd_summarize(args):
    """Summarise one or more files."""
    model = args.model
    texts = []
    for fpath in args.files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            texts.append(f"=== {fpath} ===\n{content}")
        except Exception as exc:
            print(f"  Warning: cannot read {fpath}: {exc}")

    if not texts:
        print("  No readable files provided.")
        return

    combined = "\n\n".join(texts)
    # Truncate to ~12k chars to stay within context
    if len(combined) > 12000:
        combined = combined[:12000] + "\n\n[... truncated ...]"

    prompt = (
        "Summarise the following file(s) concisely. "
        "Highlight key points, purpose, and important details:\n\n"
        + combined
    )

    print(f"\n  Model: {model}")
    print(f"  Files: {', '.join(args.files)}")
    print(f"  {'─'*50}\n")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    _stream_print(_api("/api/chat", payload, stream=True))
    print()


def cmd_review(args):
    """Review / explain code in a file."""
    model = args.model
    fpath = args.file
    try:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
    except Exception as exc:
        print(f"  Error reading {fpath}: {exc}")
        return

    if len(code) > 12000:
        code = code[:12000] + "\n\n[... truncated ...]"

    if args.explain:
        task = "Explain this code clearly. Describe what it does, how it works, and any key patterns or algorithms used."
    else:
        task = (
            "Review this code. Provide:\n"
            "1. A brief summary of what it does\n"
            "2. Potential bugs or issues\n"
            "3. Security concerns (if any)\n"
            "4. Suggestions for improvement\n"
            "5. Code quality rating (1-10)"
        )

    prompt = f"{task}\n\nFile: {fpath}\n```\n{code}\n```"

    action = "Explaining" if args.explain else "Reviewing"
    print(f"\n  {action}: {fpath}")
    print(f"  Model: {model}")
    print(f"  {'─'*50}\n")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    _stream_print(_api("/api/chat", payload, stream=True))
    print()


def cmd_generate(args):
    """Generate code from a description."""
    model = args.model
    description = " ".join(args.description)
    lang = args.lang or "python"

    prompt = (
        f"Generate {lang} code for the following task. "
        f"Provide only the code with brief comments, no extra explanation.\n\n"
        f"Task: {description}"
    )

    print(f"\n  Generating {lang} code...")
    print(f"  Model: {model}")
    print(f"  {'─'*50}\n")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    result = _stream_print(_api("/api/chat", payload, stream=True))
    print()

    if args.output:
        # Extract code block if present
        code = result
        if "```" in result:
            blocks = result.split("```")
            for i, block in enumerate(blocks):
                if i % 2 == 1:  # odd indices are code blocks
                    # Remove language identifier on first line
                    lines = block.split("\n")
                    if lines and not lines[0].strip().startswith(("#", "/", "import", "def", "class", "from")):
                        lines = lines[1:]
                    code = "\n".join(lines).strip()
                    break

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(code + "\n")
        print(f"  Saved to: {args.output}\n")


def cmd_ask(args):
    """Ask a single question and get an answer."""
    model = args.model
    question = " ".join(args.question)

    # Optionally include file context
    context = ""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if len(content) > 12000:
                content = content[:12000] + "\n\n[... truncated ...]"
            context = f"\n\nContext from {args.file}:\n```\n{content}\n```"
        except Exception as exc:
            print(f"  Warning: cannot read {args.file}: {exc}")

    prompt = question + context

    print(f"\n  Model: {model}")
    print(f"  {'─'*50}\n")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    _stream_print(_api("/api/chat", payload, stream=True))
    print()


# ── CLI entry ────────────────────────────────────────────────────────

def run(argv=None):
    p = argparse.ArgumentParser(
        prog="devtoolkit ai",
        description="AI assistant powered by Ollama (local LLM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Setup:
              1. Install Ollama: https://ollama.com/download
              2. Start server:   ollama serve
              3. Pull a model:   python -m devtoolkit ai pull llama3

            Examples:
              python -m devtoolkit ai models
              python -m devtoolkit ai chat
              python -m devtoolkit ai chat -p "Explain Python decorators"
              python -m devtoolkit ai ask "What is a binary tree?"
              python -m devtoolkit ai summarize README.md src/main.py
              python -m devtoolkit ai review app.py
              python -m devtoolkit ai review app.py --explain
              python -m devtoolkit ai generate "REST API with Flask" --lang python
              python -m devtoolkit ai generate "merge sort" -o sort.py

            Environment:
              OLLAMA_HOST   Ollama server URL (default: http://localhost:11434)
        """),
    )
    sub = p.add_subparsers(dest="command")

    # ── models ──
    sub_models = sub.add_parser("models", help="List locally available models")

    # ── pull ──
    sub_pull = sub.add_parser("pull", help="Pull / download a model")
    sub_pull.add_argument("model_name", help="Model name (e.g. llama3, mistral, codellama)")

    # ── chat ──
    sub_chat = sub.add_parser("chat", help="Interactive chat (or single prompt with -p)")
    sub_chat.add_argument("-m", "--model", default="llama3", help="Model name (default: llama3)")
    sub_chat.add_argument("-p", "--prompt", nargs="+", help="Single prompt (skip interactive mode)")
    sub_chat.add_argument("-s", "--system", help="System prompt to set AI behaviour")

    # ── ask ──
    sub_ask = sub.add_parser("ask", help="Ask a single question")
    sub_ask.add_argument("question", nargs="+", help="Your question")
    sub_ask.add_argument("-m", "--model", default="llama3", help="Model name")
    sub_ask.add_argument("-f", "--file", help="Include file as context")

    # ── summarize ──
    sub_sum = sub.add_parser("summarize", help="Summarise one or more files")
    sub_sum.add_argument("files", nargs="+", help="Files to summarise")
    sub_sum.add_argument("-m", "--model", default="llama3", help="Model name")

    # ── review ──
    sub_rev = sub.add_parser("review", help="Review or explain code in a file")
    sub_rev.add_argument("file", help="File to review")
    sub_rev.add_argument("-m", "--model", default="llama3", help="Model name")
    sub_rev.add_argument("--explain", action="store_true", help="Explain instead of review")

    # ── generate ──
    sub_gen = sub.add_parser("generate", help="Generate code from a description")
    sub_gen.add_argument("description", nargs="+", help="What to generate")
    sub_gen.add_argument("-m", "--model", default="llama3", help="Model name")
    sub_gen.add_argument("-l", "--lang", default="python", help="Programming language")
    sub_gen.add_argument("-o", "--output", help="Save generated code to file")

    args = p.parse_args(argv)

    if not args.command:
        p.print_help()
        return 0

    cmds = {
        "models": cmd_models,
        "pull": cmd_pull,
        "chat": cmd_chat,
        "ask": cmd_ask,
        "summarize": cmd_summarize,
        "review": cmd_review,
        "generate": cmd_generate,
    }
    return cmds[args.command](args)
