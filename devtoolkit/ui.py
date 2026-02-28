"""Tkinter desktop UI wrapper for DevToolKit CLI tools."""

from __future__ import annotations

import argparse
import queue
import shlex
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk


TOOL_CHOICES = [
    ("organize", "Organize files by type/extension"),
    ("dupes", "Find duplicate files by content hash"),
    ("password", "Generate strong passwords"),
    ("convert", "Convert JSON <-> CSV"),
    ("search", "Search text/regex in files"),
    ("sysinfo", "Display detailed system information"),
    ("todo", "Manage local todos"),
    ("hash", "Compute hashes for files/text"),
    ("timestamp", "Convert timestamps and dates"),
    ("serve", "Start quick HTTP file server"),
    ("regex", "Test regex patterns"),
    ("snippet", "Manage reusable code snippets"),
    ("encode", "Encode/decode values"),
    ("diff", "Compare two files"),
    ("lorem", "Generate Lorem Ipsum text"),
    ("ai", "Local AI helper via Ollama"),
]


class DevToolKitUI:
    """A thin GUI wrapper around existing CLI tools."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("DevToolKit UI")
        self.root.geometry("940x620")
        self.root.minsize(760, 480)

        self.output_queue: queue.Queue[str] = queue.Queue()
        self.running_process: subprocess.Popen[str] | None = None

        self._build_ui()
        self.root.after(80, self._drain_output_queue)

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top = ttk.Frame(self.root, padding=12)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Tool").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.tool_var = tk.StringVar(value=TOOL_CHOICES[0][0])
        self.tool_combo = ttk.Combobox(
            top,
            textvariable=self.tool_var,
            state="readonly",
            values=[name for name, _ in TOOL_CHOICES],
        )
        self.tool_combo.grid(row=0, column=1, sticky="ew")
        self.tool_combo.bind("<<ComboboxSelected>>", self._update_tool_hint)

        ttk.Label(top, text="Args").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(10, 0))
        self.args_var = tk.StringVar()
        self.args_entry = ttk.Entry(top, textvariable=self.args_var)
        self.args_entry.grid(row=1, column=1, sticky="ew", pady=(10, 0))

        button_row = ttk.Frame(top)
        button_row.grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.run_button = ttk.Button(button_row, text="Run", command=self.run_selected_tool)
        self.run_button.grid(row=0, column=0, padx=(0, 8))
        self.stop_button = ttk.Button(button_row, text="Stop", command=self.stop_running_tool, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 8))
        ttk.Button(button_row, text="Clear", command=self.clear_output).grid(row=0, column=2)

        self.hint_var = tk.StringVar()
        self.hint_label = ttk.Label(top, textvariable=self.hint_var, foreground="#555555")
        self.hint_label.grid(row=3, column=1, sticky="w", pady=(10, 0))
        self._update_tool_hint()

        output_frame = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        output_frame.grid(row=1, column=0, sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="word", font=("Consolas", 10))
        self.output_text.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scroll.set)

        self.output_text.insert(
            "end",
            "DevToolKit UI ready.\n"
            "Choose a tool, enter args (same as CLI), then click Run.\n\n"
            "Examples:\n"
            "  tool=search  args=\"TODO . --ignore-case\"\n"
            "  tool=password  args=\"--length 24 --count 3\"\n"
            "  tool=timestamp args=\"now --add 2d\"\n\n",
        )
        self.output_text.see("end")

    def _update_tool_hint(self, _event: object | None = None) -> None:
        selected = self.tool_var.get()
        description = next((desc for name, desc in TOOL_CHOICES if name == selected), "")
        self.hint_var.set(f"{selected}: {description}")

    def _append_output(self, text: str) -> None:
        self.output_text.insert("end", text)
        self.output_text.see("end")

    def clear_output(self) -> None:
        self.output_text.delete("1.0", "end")

    def run_selected_tool(self) -> None:
        if self.running_process is not None:
            self._append_output("A command is already running. Stop it first.\n")
            return

        tool = self.tool_var.get()
        raw_args = self.args_var.get().strip()
        try:
            extra_args = shlex.split(raw_args, posix=False) if raw_args else []
        except ValueError as exc:
            self._append_output(f"Argument parse error: {exc}\n")
            return

        cmd = [sys.executable, "-m", "devtoolkit", tool, *extra_args]
        self._append_output(f"\n$ {' '.join(cmd)}\n")
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        thread = threading.Thread(target=self._run_command_thread, args=(cmd,), daemon=True)
        thread.start()

    def _run_command_thread(self, cmd: list[str]) -> None:
        try:
            self.running_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            assert self.running_process.stdout is not None
            for line in self.running_process.stdout:
                self.output_queue.put(line)
            returncode = self.running_process.wait()
            self.output_queue.put(f"\n[exit code: {returncode}]\n")
        except Exception as exc:
            self.output_queue.put(f"\nFailed to run command: {exc}\n")
        finally:
            self.running_process = None
            self.output_queue.put("__CMD_DONE__")

    def stop_running_tool(self) -> None:
        if self.running_process is None:
            return
        self.running_process.terminate()
        self._append_output("\n[termination requested]\n")

    def _drain_output_queue(self) -> None:
        while True:
            try:
                chunk = self.output_queue.get_nowait()
            except queue.Empty:
                break
            if chunk == "__CMD_DONE__":
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
            else:
                self._append_output(chunk)
        self.root.after(80, self._drain_output_queue)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="devtoolkit ui",
        description="Launch a desktop GUI wrapper for DevToolKit.",
    )
    parser.parse_args(argv)

    root = tk.Tk()
    app = DevToolKitUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: _on_close(root, app))
    root.mainloop()
    return 0


def _on_close(root: tk.Tk, app: DevToolKitUI) -> None:
    if app.running_process is not None:
        app.running_process.terminate()
    root.destroy()
