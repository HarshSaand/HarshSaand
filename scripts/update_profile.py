#!/usr/bin/env python3
"""Refresh the recent-work block in the profile README."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


START = "<!-- RECENT_WORK:START -->"
END = "<!-- RECENT_WORK:END -->"
OWNER = "HarshSaand"
PROFILE_REPO = OWNER.lower()
MAX_REPOS = 6
DISPLAY_NAMES = {
    "deepshield-approvalguard": "DeepShield ApprovalGuard",
    "lithotwin-ai-tcad": "LithoTwin AI TCAD",
    "local-multilingual-speech-intelligence": "Local Multilingual Speech Intelligence",
    "Multi-Agent-Tile-PJ": "Multi-Agent Tileworld",
    "processtwin-ai-tcad": "ProcessTwin AI TCAD",
    "wafer-process-signature-triage": "Wafer Process Signature Triage",
}


def fetch_repositories(owner: str = OWNER) -> list[dict[str, Any]]:
    url = f"https://api.github.com/users/{owner}/repos?per_page=100&type=owner&sort=pushed"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{owner}-profile-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not load GitHub repositories: {error}") from error

    if not isinstance(payload, list):
        raise RuntimeError("GitHub returned an unexpected repository payload")
    return payload


def select_repositories(repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eligible = [
        repo
        for repo in repositories
        if not repo.get("private")
        and not repo.get("fork")
        and not repo.get("archived")
        and repo.get("name", "").lower() != PROFILE_REPO
        and str(repo.get("description") or "").strip()
    ]
    eligible.sort(key=lambda repo: repo.get("pushed_at") or "", reverse=True)
    return eligible[:MAX_REPOS]


def readable_date(timestamp: str | None) -> str:
    if not timestamp:
        return "date unavailable"
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%b %Y")


def render_feed(repositories: list[dict[str, Any]]) -> str:
    if not repositories:
        return "_No described public projects are available yet._"

    entries: list[str] = []
    for repo in repositories:
        name = DISPLAY_NAMES.get(repo["name"], repo["name"].replace("-", " ").title())
        link = repo["html_url"]
        description = str(repo["description"]).strip().rstrip(".")
        language = repo.get("language") or "Mixed stack"
        topics = [str(topic).replace("-", " ") for topic in repo.get("topics", [])[:2]]
        metadata = " / ".join([language, *topics, readable_date(repo.get("pushed_at"))])
        entries.append(f"**[{name}]({link})**<br>\n{description}.<br>\n<sub>{metadata}</sub>")
    return "\n\n".join(entries)


def replace_feed(readme: str, feed: str) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one recent-work marker pair")
    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)
    return f"{before}{START}\n{feed}\n{END}{after}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--repos-json", type=Path, help="Use a local API response instead of the network")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.repos_json:
        repositories = json.loads(args.repos_json.read_text(encoding="utf-8"))
    else:
        repositories = fetch_repositories()

    selected = select_repositories(repositories)
    original = args.readme.read_text(encoding="utf-8")
    updated = replace_feed(original, render_feed(selected))
    args.readme.write_text(updated, encoding="utf-8")
    print(f"Updated {args.readme} with {len(selected)} repositories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
