"""Shared yt-dlp settings for preview and downloads."""

import os
import sys


def yt_dlp_options():
    # Release builds bundle Deno; source installs can use Deno from PATH.
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir:
        filename = "deno.exe" if os.name == "nt" else "deno"
        deno = os.path.join(bundle_dir, "deno", filename)
        if os.path.isfile(deno):
            return {"js_runtimes": {"deno": {"path": deno}}}
    return {}


def video_format(quality):
    height = next((n for n in (1080, 720, 480, 360) if f"{n}p" in quality), None)
    limit = f"[height<={height}]" if height else ""
    # Prefer MP4 streams, with a resolution-limited fallback when a video
    # offers only other codecs.
    return (
        f"bestvideo[ext=mp4]{limit}+bestaudio[ext=m4a]/"
        f"best[ext=mp4]{limit}/"
        f"bestvideo{limit}+bestaudio/"
        f"best{limit}"
    )
