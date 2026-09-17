"""Build a release with the JavaScript runtime needed by yt-dlp."""

import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

os.environ.setdefault("PYINSTALLER_CONFIG_DIR", os.path.join(tempfile.gettempdir(), "youtube-downloader-pro-pyi"))
import PyInstaller.__main__


deno = shutil.which("deno")
if not deno:
    raise SystemExit("Deno is required to build a release: https://deno.com/")

platform_name = {"darwin": "macOS", "win32": "Windows"}.get(sys.platform, "Linux")
name = f"YTDownloader-{platform_name}" if platform_name != "macOS" else "YTDownloader"
arguments = [
    "app.py",
    "--name", name,
    "--noconsole",
    "--noconfirm",
    "--collect-all", "yt_dlp_ejs",
    "--add-binary", f"{deno}{os.pathsep}deno",
]
if platform_name == "macOS":
    arguments += ["--windowed", "--icon", "icon.icns"]
else:
    arguments += ["--onefile"]
    if platform_name == "Windows":
        arguments += ["--icon", "icon.ico"]

release_version = os.environ.get("APP_RELEASE_VERSION")
version_file = Path(__file__).with_name("version.py")
original_version = None
if release_version:
    if not re.fullmatch(r"v\d+(?:\.\d+)*", release_version):
        raise SystemExit("APP_RELEASE_VERSION must look like v2026.09.17.1")
    original_version = version_file.read_text(encoding="utf-8")
    version_file.write_text(f"APP_VERSION = {release_version!r}\n", encoding="utf-8")

try:
    PyInstaller.__main__.run(arguments)
finally:
    if original_version is not None:
        version_file.write_text(original_version, encoding="utf-8")
