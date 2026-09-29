#!/usr/bin/env python3
"""update.py — fetch the latest make-lecture-kit, so every user stays current.

The maintainer publishes new versions; each user runs this once in a while to
pull the newest kit. It tries two ways, in order:

  1. git  — if this kit is a git clone, just `git pull`.
  2. a published zip — download  <SOURCE>/VERSION  and  <SOURCE>/make-lecture-kit.zip
     where <SOURCE> is the base URL in `update_source.txt` (the instructor sets it
     once before sharing).

Generating companions NEVER needs the network. This command is the only part that
does, and only when you run it on purpose. Your own work in `output/` is never
touched. Pure standard library.

Usage:
    python3 scripts/update.py            # install the latest if newer
    python3 scripts/update.py --check    # only compare versions, change nothing
    python3 scripts/update.py --force    # reinstall even if versions match
"""

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kp(*parts):
    return os.path.join(ROOT, *parts)


def local_version():
    try:
        return open(kp("VERSION"), encoding="utf-8").read().strip()
    except OSError:
        return "0.0.0"


def read_source():
    """The base URL the instructor publishes to (or '' if not set)."""
    f = kp("update_source.txt")
    if not os.path.isfile(f):
        return ""
    for line in open(f, encoding="utf-8"):
        s = line.strip()
        if s and not s.startswith("#") and "PUT-YOUR" not in s:
            return s.rstrip("/")
    return ""


def resolve_source(src):
    """Turn the configured source into (version_url, zip_url, label).

    A plain GitHub repo URL is understood natively: we read VERSION over 'raw'
    and download the auto-generated zip of the default branch — so the instructor
    just pushes normally, nothing extra to host. Any other value is treated as a
    base URL serving <base>/VERSION and <base>/make-lecture-kit.zip.
    """
    s = src.strip().rstrip("/")
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", s)
    if m:
        user, repo = m.group(1), m.group(2)
        branch = "main"
        ver = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/VERSION"
        zipu = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
        return ver, zipu, f"GitHub {user}/{repo}@{branch}"
    return s + "/VERSION", s + "/make-lecture-kit.zip", s


def vtuple(v):
    out = []
    for x in v.split("."):
        try:
            out.append(int(x))
        except ValueError:
            out.append(0)
    return tuple(out)


def http_get(url, timeout=60):
    req = urllib.request.Request(
        url, headers={"User-Agent": "make-lecture-kit-update"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read()


def try_git():
    """Return True/False if this is a git clone, else None (not a repo)."""
    if not os.path.isdir(kp(".git")) or shutil.which("git") is None:
        return None
    print("[update] git clone detected — running 'git pull' ...")
    r = subprocess.run(["git", "pull", "--ff-only"], cwd=ROOT,
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip())
    return r.returncode == 0


def install_zip(data):
    """Extract the downloaded kit over this one, preserving output/."""
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            z.extractall(td)
        src = None
        for dirpath, _dirs, files in os.walk(td):
            if "SKILL.md" in files:
                src = dirpath
                break
        if src is None:
            print("[update] the downloaded archive has no SKILL.md — aborting.")
            return False
        copied = 0
        for name in os.listdir(src):
            if name == "output":          # never clobber the user's own work
                continue
            s = os.path.join(src, name)
            d = kp(name)
            if os.path.isdir(s):
                shutil.rmtree(d, ignore_errors=True)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
            copied += 1
        print(f"[update] refreshed {copied} item(s) from the latest release.")
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="only compare versions; change nothing")
    ap.add_argument("--force", action="store_true",
                    help="reinstall even if versions match")
    args = ap.parse_args()

    cur = local_version()
    print(f"[update] current version: {cur}")

    # 1) git clone -> git pull
    if not args.check:
        g = try_git()
        if g is True:
            print(f"[update] now at version {local_version()}.  Done.")
            return 0
        if g is False:
            print("[update] git pull did not complete; trying a published zip ...")

    # 2) published zip
    base = read_source()
    if not base:
        print("[update] No update source is set yet.")
        print("         Your instructor publishes updates and sets the URL in")
        print("         update_source.txt — or shares a git repo to clone.")
        print("         Ask them for the latest link, or re-download the kit.")
        return 0 if args.check else 1

    version_url, zip_url, label = resolve_source(base)
    print(f"[update] source: {label}")
    try:
        remote = http_get(version_url).decode("utf-8").strip()
    except Exception as exc:  # noqa: BLE001
        print(f"[update] could not reach the source ({exc}). Are you online?")
        return 1
    print(f"[update] latest available: {remote}")

    if not args.force and vtuple(remote) <= vtuple(cur):
        print("[update] you already have the latest.  Done.")
        return 0
    if args.check:
        print("[update] a newer version exists — run without --check to install.")
        return 0

    print("[update] downloading the latest kit ...")
    try:
        data = http_get(zip_url, timeout=180)
    except Exception as exc:  # noqa: BLE001
        print(f"[update] download failed ({exc}).")
        return 1
    if install_zip(data):
        print(f"[update] updated {cur} -> {local_version()}.  See CHANGELOG.md.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
