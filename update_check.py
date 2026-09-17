"""Check public GitHub releases without blocking the Tk event loop."""

import re

import requests


RELEASES_API = "https://api.github.com/repos/valvdov/YouTubeDownloaderPro/releases/latest"
RELEASES_PAGE = "https://github.com/valvdov/YouTubeDownloaderPro/releases/latest"


def version_numbers(value):
    match = re.fullmatch(r"v?(\d+(?:\.\d+)*)", value)
    return tuple(int(part) for part in match.group(1).split(".")) if match else None


def newer_release(current_version, release):
    current = version_numbers(current_version)
    latest = version_numbers(release.get("tag_name", ""))
    if current is None or latest is None:
        return False
    length = max(len(current), len(latest))
    return current + (0,) * (length - len(current)) < latest + (0,) * (length - len(latest))


def find_update(current_version):
    """Return a newer public release, or None when offline or up to date."""
    if version_numbers(current_version) is None:
        return None
    try:
        response = requests.get(
            RELEASES_API,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "YouTubeDownloaderPro"},
            timeout=6,
        )
        response.raise_for_status()
        release = response.json()
    except (requests.RequestException, ValueError):
        return None
    if not isinstance(release, dict):
        return None
    return release if newer_release(current_version, release) else None
