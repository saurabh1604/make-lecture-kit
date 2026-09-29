#!/usr/bin/env bash
# publish.sh — release a new version of make-lecture-kit so everyone can fetch it.
#
# Run from the kit root AFTER you've (1) made your change, (2) bumped VERSION,
# and (3) added a CHANGELOG entry. It self-checks, commits, and pushes; users
# then get it with `python3 scripts/update.py` (or `git pull`).
set -e
cd "$(cd "$(dirname "$0")" && pwd)"

echo "==> Health check"
python3 scripts/selfcheck.py

ver="$(cat VERSION)"
echo "==> Releasing v${ver}"

if [ ! -d .git ]; then
  echo "No git repo yet. First-time setup:"
  echo "  git init -b main && git add -A && git commit -m \"release v${ver}\""
  echo "  git remote add origin https://github.com/saurabh1604/make-lecture-kit.git"
  echo "  git push -u origin main   (create the empty repo on github.com first)"
  exit 1
fi

git add -A
git commit -m "release v${ver}" || echo "(nothing new to commit)"
git push
echo "==> Done. Users update with:  python3 scripts/update.py"
