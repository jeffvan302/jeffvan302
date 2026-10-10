#!/usr/bin/env python3
"""Rebuild the "Most Used Languages" block in README.md.

Sums the language byte counts GitHub reports for the owner's public,
non-fork repositories, then writes:
  * assets/languages/pie.svg        - pie chart (no text, so it reads in light and dark mode)
  * assets/languages/<slug>.svg     - one small colour swatch per listed language
  * README.md                       - an HTML table between the LANGUAGES markers

Standard library only. Configuration comes from environment variables:
  GITHUB_TOKEN      token for the GitHub REST API (the workflow's built-in token is enough)
  GH_USERNAME       account to summarise (default: GITHUB_REPOSITORY_OWNER)
  TOP_N             languages listed before grouping the rest as "Other" (default 8)
  EXCLUDE_LANGS     comma-separated languages to ignore (e.g. "Jupyter Notebook,HTML")
  EXCLUDE_REPOS     comma-separated repository names to ignore (default: the profile repo)

For local testing, pass --fixture data.json where the file maps
{"repo-name": {"Language": bytes, ...}, ...}; no network calls are made for repo data.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
ASSETS = ROOT / "assets" / "languages"
START, END = "<!-- LANGUAGES:START -->", "<!-- LANGUAGES:END -->"
LINGUIST_URL = "https://raw.githubusercontent.com/github-linguist/linguist/main/lib/linguist/languages.yml"
OTHER_COLOR = "#8b949e"
FALLBACK_COLORS = {
    "C#": "#7355dd", "C++": "#f34b7d", "C": "#555555", "Python": "#3572A5",
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Jupyter Notebook": "#DA5B0B",
    "HTML": "#e34c26", "CSS": "#663399", "Visual Basic .NET": "#945db7",
    "PowerShell": "#012456", "Shell": "#89e051", "Batchfile": "#C1F12E",
    "Dockerfile": "#384d54", "SQL": "#e38c00", "TSQL": "#e38c00",
}


def api_get(url: str, token: str | None):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-language-stats",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_language_bytes(user: str, token: str | None, exclude_repos: set[str]) -> dict[str, dict[str, int]]:
    repos, page = [], 1
    while True:
        batch = api_get(f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}", token)
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    data = {}
    for repo in repos:
        if repo.get("fork") or repo.get("private") or repo["name"] in exclude_repos:
            continue
        data[repo["name"]] = api_get(repo["languages_url"], token)
    return data


def load_linguist_colors() -> dict[str, str]:
    """Parse just the `color:` of each top-level language in linguist's languages.yml."""
    colors = dict(FALLBACK_COLORS)
    try:
        with urllib.request.urlopen(LINGUIST_URL, timeout=30) as resp:
            text = resp.read().decode("utf-8")
    except Exception as exc:  # network trouble: fall back to the built-in colours
        print(f"warning: could not load linguist colours ({exc}); using fallbacks", file=sys.stderr)
        return colors
    current = None
    for line in text.splitlines():
        top = re.match(r'^("?)([^\s#"][^"]*?)\1:\s*$', line)
        if top:
            current = top.group(2)
            continue
        col = re.match(r'^\s+color:\s*"(#[0-9a-fA-F]{6})"', line)
        if col and current:
            colors[current] = col.group(1)
    return colors


def slugify(name: str) -> str:
    name = name.replace("#", "-sharp").replace("+", "p")
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "lang"


def summarise(data: dict[str, dict[str, int]], top_n: int, exclude_langs: set[str]):
    totals: dict[str, int] = {}
    for langs in data.values():
        for lang, size in langs.items():
            if lang not in exclude_langs:
                totals[lang] = totals.get(lang, 0) + int(size)
    grand = sum(totals.values())
    if grand == 0:
        return []
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    rows = [(lang, size / grand * 100) for lang, size in ranked[:top_n]]
    rest = sum(size for _, size in ranked[top_n:])
    if rest:
        rows.append(("Other", rest / grand * 100))
    return rows


def pie_svg(rows, colors) -> str:
    size, r = 200, 98
    cx = cy = size / 2
    parts = []
    if len(rows) == 1:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colors[rows[0][0]]}"/>')
    else:
        angle = -math.pi / 2
        for lang, pct in rows:
            sweep = pct / 100 * 2 * math.pi
            x1, y1 = cx + r * math.cos(angle), cy + r * math.sin(angle)
            angle += sweep
            x2, y2 = cx + r * math.cos(angle), cy + r * math.sin(angle)
            large = 1 if sweep > math.pi else 0
            parts.append(
                f'<path d="M{cx},{cy} L{x1:.2f},{y1:.2f} A{r},{r} 0 {large} 1 {x2:.2f},{y2:.2f} Z" '
                f'fill="{colors[lang]}"><title>{lang} {pct:.1f}%</title></path>'
            )
    body = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        f'role="img" aria-label="Most used languages">\n  '
        f'<g stroke="#000000" stroke-opacity="0.25" stroke-width="1" stroke-linejoin="round">\n  {body}\n  </g>\n</svg>\n'
    )


def swatch_svg(color: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12">'
        f'<rect width="12" height="12" rx="3" fill="{color}"/></svg>\n'
    )


def render_block(rows, slugs, user: str) -> str:
    link = f"https://github.com/{user}?tab=repositories"
    lines = [
        START,
        '<table align="center">',
        "<tr>",
        f'<td><a href="{link}"><img src="assets/languages/pie.svg" alt="Pie chart of most used languages" width="200" height="200" /></a></td>',
        "<td>",
        "<table>",
        '<tr><th></th><th align="left">Language</th><th align="right">Share</th></tr>',
    ]
    for lang, pct in rows:
        lines.append(
            f'<tr><td><a href="{link}"><img src="assets/languages/{slugs[lang]}.svg" alt="" width="12" height="12" /></a></td>'
            f'<td>{lang}</td><td align="right">{pct:.1f}%</td></tr>'
        )
    lines += [
        "</table>",
        "</td>",
        "</tr>",
        "</table>",
        '<p align="center"><sub>Most used languages across my public repositories, by code size · updated daily</sub></p>',
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixture", type=Path, help="JSON file of per-repo language bytes (skips the GitHub API)")
    args = parser.parse_args()

    user = os.environ.get("GH_USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER")
    if not user:
        print("Set GH_USERNAME (or run inside GitHub Actions).", file=sys.stderr)
        return 1
    top_n = int(os.environ.get("TOP_N", "8"))
    split = lambda v: {s.strip() for s in v.split(",") if s.strip()}
    exclude_langs = split(os.environ.get("EXCLUDE_LANGS", ""))
    exclude_repos = split(os.environ.get("EXCLUDE_REPOS", user))

    if args.fixture:
        data = json.loads(args.fixture.read_text())
    else:
        data = fetch_language_bytes(user, os.environ.get("GITHUB_TOKEN"), exclude_repos)

    rows = summarise(data, top_n, exclude_langs)
    if not rows:
        print("No language data found; README left unchanged.")
        return 0

    colors = load_linguist_colors()
    colors["Other"] = OTHER_COLOR
    for lang, _ in rows:
        colors.setdefault(lang, OTHER_COLOR)

    ASSETS.mkdir(parents=True, exist_ok=True)
    slugs = {lang: slugify(lang) for lang, _ in rows}
    keep = {"pie.svg"} | {f"{s}.svg" for s in slugs.values()}
    for old in ASSETS.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
    (ASSETS / "pie.svg").write_text(pie_svg(rows, colors))
    for lang, slug in slugs.items():
        (ASSETS / f"{slug}.svg").write_text(swatch_svg(colors[lang]))

    readme = README.read_text()
    if START not in readme or END not in readme:
        print(f"README.md is missing the {START} / {END} markers.", file=sys.stderr)
        return 1
    block = render_block(rows, slugs, user)
    updated = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S)
    README.write_text(updated)

    for lang, pct in rows:
        print(f"{lang:<20} {pct:5.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
