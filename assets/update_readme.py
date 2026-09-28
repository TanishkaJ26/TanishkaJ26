"""Adds new GitHub repos to the README as project cards.

Fetches public repos for USER, skips the hand-written ones (FEATURED) and anything in
EXCLUDE, draws a card per repo into assets/auto/, and rewrites the block between the
AUTO-PROJECTS markers in README.md. Runs in .github/workflows/update-readme.yml.

Run from the repo root:  python assets/update_readme.py
"""
import html
import json
import os
import re
import sys
import textwrap
import urllib.request
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_readme_svgs import AMBER, BLUE, OUT, TEAL, project  # noqa: E402

USER = "TanishkaJ26"

# Already on the README with hand-written copy.
FEATURED = {"tanishkaj26", "bgpshield", "spotlight", "wanderlust", "dsa-cpp"}

# Public repos to keep off the README. Remove a name to let it show up.
EXCLUDE = {"portfolio", "makemytrip-clone-"}

MAX_CARDS = 6
ACCENTS = [BLUE, TEAL, AMBER, "#c9a7ff", "#ff9fb2"]

ROOT = os.path.dirname(OUT)
README = os.path.join(ROOT, "README.md")
AUTO_DIR = os.path.join(OUT, "auto")
START, END = "<!-- AUTO-PROJECTS:START -->", "<!-- AUTO-PROJECTS:END -->"


def fetch_repos():
    url = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=created"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pick(repos):
    keep = [r for r in repos
            if not r["fork"] and not r["archived"] and not r["private"]
            and r["name"].lower() not in FEATURED | EXCLUDE]
    keep.sort(key=lambda r: r["created_at"], reverse=True)
    return keep[:MAX_CARDS]


def clean(text):
    # No em dashes on this profile.
    return re.sub(r"\s*[—–]\s*", ", ", text or "").strip()


def esc(text):
    return html.escape(text, quote=False)


def describe(repo):
    desc = clean(repo["description"]) or f"{repo['language'] or 'Code'} project. Description coming soon."
    lines = textwrap.wrap(desc, 46)
    if len(lines) > 3:
        lines = lines[:2] + [textwrap.shorten(" ".join(lines[2:]), 45, placeholder="…")]
    return lines


def slug(name):
    return re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")


def accent(name):
    # Keyed on the repo name so a card keeps its colour when others come and go.
    return ACCENTS[zlib.crc32(name.lower().encode()) % len(ACCENTS)]


def build_cards(repos):
    os.makedirs(AUTO_DIR, exist_ok=True)
    wanted = set()
    for i, r in enumerate(repos):
        fname = f"{slug(r['name'])}.svg"
        wanted.add(fname)
        chips = [c for c in [r["language"], *r.get("topics", [])] if c][:4]
        project(f"auto/{fname}", esc(r["name"]), accent(r["name"]), [esc(l) for l in describe(r)],
                [esc(c) for c in chips],
                f"github.com/{USER}/{r['name']}", offset=(i % 2) * 0.8, live=bool(r["homepage"]))
    for f in os.listdir(AUTO_DIR):
        if f.endswith(".svg") and f not in wanted:
            os.remove(os.path.join(AUTO_DIR, f))


def block(repos):
    if not repos:
        return f"{START}\n{END}"
    cards = "\n".join(
        f'  <a href="{r["html_url"]}"><img src="./assets/auto/{slug(r["name"])}.svg" width="49%" '
        f'alt="{html.escape(r["name"])}. {html.escape(" ".join(describe(r)))}" /></a>'
        for r in repos)
    live = [f'<a href="{html.escape(r["homepage"])}">{html.escape(r["name"])}</a>' for r in repos if r["homepage"]]
    live_line = f'\n\n<p align="center">\n  Live: {" · ".join(live)}\n</p>' if live else ""
    return (f"{START}\n"
            f'<img src="./assets/section-more.svg" width="100%" alt="03 More Work. Newest first. Added automatically." />\n\n'
            f'<p align="center">\n{cards}\n</p>{live_line}\n'
            f"{END}")


def main():
    repos = pick(fetch_repos())
    build_cards(repos)
    with open(README, encoding="utf-8") as f:
        readme = f.read()
    if START not in readme or END not in readme:
        sys.exit(f"README.md is missing the {START} / {END} markers.")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block(repos), readme, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    print(f"{len(repos)} auto project(s): {', '.join(r['name'] for r in repos) or 'none'}")


if __name__ == "__main__":
    main()
