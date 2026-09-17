"""Clipboard shortcuts for the URL field, independent of keyboard layout."""

import sys
import tkinter as tk


def paste_into_entry(entry):
    """Replace the current selection, or insert at the cursor."""
    try:
        value = entry.clipboard_get()
    except tk.TclError:
        return "break"

    try:
        start, end = entry.index("sel.first"), entry.index("sel.last")
    except tk.TclError:
        start = end = entry.index(tk.INSERT)

    if start != end:
        entry.delete(start, end)
    entry.insert(start, value)
    entry.icursor(start + len(value))
    return "break"


def select_all_in_entry(entry):
    """Select the complete URL so the next paste replaces it."""
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    return "break"


def install_paste_handler(entry):
    """Handle Command/Ctrl+A and V before layout-dependent Tk bindings."""
    modifier = 0x0008 if sys.platform == "darwin" else 0x0004

    def on_key(event):
        # Russian М is on the same physical key as Latin V. The keycode
        # catches other layouts on macOS and Windows as well.
        paste_key = event.keysym.lower() in {"v", "м", "cyrillic_em"}
        if sys.platform == "darwin":
            paste_key |= event.keycode == 9
        elif sys.platform == "win32":
            paste_key |= event.keycode == 86
        select_key = event.keysym.lower() in {"a", "ф", "cyrillic_ef"}
        if sys.platform == "darwin":
            select_key |= event.keycode == 0
        elif sys.platform == "win32":
            select_key |= event.keycode == 65
        if event.state & modifier:
            if paste_key:
                return paste_into_entry(entry)
            if select_key:
                return select_all_in_entry(entry)
        return None

    entry.bind("<KeyPress>", on_key)
    entry.bind("<<Paste>>", lambda _event: paste_into_entry(entry))
    entry.bind("<<SelectAll>>", lambda _event: select_all_in_entry(entry))
