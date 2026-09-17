import os
import sys
import tkinter as tk
import unittest
from unittest.mock import patch

from download_support import video_format, yt_dlp_options
from paste_support import install_paste_handler, paste_into_entry, select_all_in_entry
from update_check import find_update, newer_release


class FakeEntry:
    def __init__(self, text="", clipboard="", selection=None, cursor=None):
        self.text = text
        self.clipboard = clipboard
        self.selection = selection
        self.cursor = len(text) if cursor is None else cursor
        self.bindings = {}

    def clipboard_get(self):
        if self.clipboard is None:
            raise tk.TclError("empty clipboard")
        return self.clipboard

    def index(self, position):
        if position == "sel.first":
            if self.selection is None:
                raise tk.TclError("no selection")
            return self.selection[0]
        if position == "sel.last":
            return self.selection[1]
        return self.cursor

    def delete(self, start, end):
        self.text = self.text[:start] + self.text[end:]

    def insert(self, start, value):
        self.text = self.text[:start] + value + self.text[start:]

    def icursor(self, position):
        self.cursor = len(self.text) if position == tk.END else position

    def select_range(self, start, end):
        self.selection = (start, len(self.text) if end == tk.END else end)

    def bind(self, pattern, callback):
        self.bindings[pattern] = callback


class PasteTests(unittest.TestCase):
    def test_paste_replaces_selection(self):
        entry = FakeEntry("old video ID", "new ID", (0, 12))
        self.assertEqual(paste_into_entry(entry), "break")
        self.assertEqual(entry.text, "new ID")
        self.assertEqual(entry.cursor, 6)

    def test_paste_inserts_at_cursor(self):
        entry = FakeEntry("beforeafter", " new ", cursor=6)
        paste_into_entry(entry)
        self.assertEqual(entry.text, "before new after")

    def test_empty_clipboard_does_not_erase_selection(self):
        entry = FakeEntry("old", None, (0, 3))
        paste_into_entry(entry)
        self.assertEqual(entry.text, "old")

    def test_russian_shortcut_and_plain_typing(self):
        entry = FakeEntry("old", "new", (0, 3))
        with patch.object(sys, "platform", "darwin"):
            install_paste_handler(entry)
            event = type("Event", (), {"keysym": "м", "keycode": 9, "state": 0x0008})()
            self.assertEqual(entry.bindings["<KeyPress>"](event), "break")
            self.assertEqual(entry.text, "new")
            event.state = 0
            self.assertIsNone(entry.bindings["<KeyPress>"](event))

    def test_command_a_then_v_replaces_all(self):
        entry = FakeEntry("old video ID", "new ID")
        with patch.object(sys, "platform", "darwin"):
            install_paste_handler(entry)
            event = type("Event", (), {"keysym": "ф", "keycode": 0, "state": 0x0008})()
            self.assertEqual(entry.bindings["<KeyPress>"](event), "break")
            self.assertEqual(entry.selection, (0, len("old video ID")))
            event.keysym, event.keycode = "м", 9
            self.assertEqual(entry.bindings["<KeyPress>"](event), "break")
        self.assertEqual(entry.text, "new ID")

    def test_control_a_on_windows_and_virtual_event(self):
        entry = FakeEntry("old video ID")
        with patch.object(sys, "platform", "win32"):
            install_paste_handler(entry)
            event = type("Event", (), {"keysym": "Cyrillic_ef", "keycode": 65, "state": 0x0004})()
            self.assertEqual(entry.bindings["<KeyPress>"](event), "break")
        self.assertEqual(entry.selection, (0, len("old video ID")))
        entry.selection = None
        self.assertEqual(entry.bindings["<<SelectAll>>"](None), "break")
        self.assertEqual(entry.selection, (0, len("old video ID")))


class DownloadOptionsTests(unittest.TestCase):
    def test_resolution_fallback_stays_bounded(self):
        self.assertNotIn("/best/", video_format("720p"))
        self.assertTrue(all("[height<=720]" in part for part in video_format("720p").split("/")))

    def test_bundled_deno_path(self):
        with patch.object(sys, "_MEIPASS", "/bundle", create=True), patch("os.path.isfile", return_value=True):
            options = yt_dlp_options()
        executable = "deno.exe" if os.name == "nt" else "deno"
        self.assertEqual(options["js_runtimes"]["deno"]["path"], os.path.join("/bundle", "deno", executable))


class UpdateTests(unittest.TestCase):
    def test_only_newer_release_is_offered(self):
        release = {"tag_name": "v2026.09.21.4"}
        self.assertTrue(newer_release("v2026.09.17.3", release))
        self.assertFalse(newer_release("v2026.09.21.4", release))
        self.assertFalse(newer_release("v2026.09.22.1", release))
        self.assertFalse(newer_release("dev", release))

    def test_offline_check_does_not_interrupt_app(self):
        with patch("update_check.requests.get", side_effect=__import__("requests").RequestException):
            self.assertIsNone(find_update("v2026.09.17.1"))


if __name__ == "__main__":
    unittest.main()
