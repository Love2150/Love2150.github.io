"""Report stale or incomplete portfolio content.

The scheduled workflow uses the exit status to create or update one tracking issue:
0 means no findings, 1 means the portfolio needs review, and 2 means misuse.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

PROJECT_MAX_AGE_DAYS = 90
RESUME_MAX_AGE_DAYS = 183
HOMEPAGE_MAX_AGE_DAYS = 30


def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    marker = text.find("\n---\n", 4)
    if marker == -1:
        return {}
    values = yaml.safe_load(text[4:marker]) or {}
    return values if isinstance(values, dict) else {}


def parse_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    values = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return values if isinstance(values, dict) else {}


def parse_date(value: Any) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value).strip())
    except (TypeError, ValueError):
        return None


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def finding(category: str, target: str, message: str) -> dict[str, str]:
    return {"category": category, "target": target, "message": message}


def url_is_available(url: str, timeout: float) -> tuple[bool, str]:
    if not is_http_url(url):
        return False, "invalid HTTP(S) URL"
    headers = {"User-Agent": "Love2150-PortfolioFreshness/1.0"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                if response.status < 400:
                    return True, str(response.status)
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                continue
            return False, str(exc.code)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if method == "HEAD":
                continue
            return False, str(
                exc.reason if isinstance(exc, urllib.error.URLError) else exc
            )
    return False, "unavailable"


def safe_local_path(root: Path, url: str) -> Path | None:
    path = url.split("#", 1)[0].split("?", 1)[0]
    relative = PurePosixPath(path.lstrip("/"))
    if ".." in relative.parts:
        return None
    target = (root / Path(*relative.parts)).resolve()
    if not target.is_relative_to(root.resolve()):
        return None
    return target


def local_target_exists(root: Path, url: str, own_permalink: Any) -> bool:
    path = url.split("#", 1)[0].split("?", 1)[0]
    if path == own_permalink:
        return True
    target = safe_local_path(root, url)
    if target is None:
        return False
    candidates = (target, target / "index.html", target.with_suffix(".html"))
    return any(candidate.is_file() for candidate in candidates)


def homepage_commit_date(root: Path) -> dt.date | None:
    git = shutil.which("git")
    if git is None:
        return None
    try:
        result = subprocess.run(  # noqa: S603 - executable path is resolved with shutil.which
            [git, "log", "-1", "--format=%cs", "--", "index.html"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_date(result.stdout.strip())


def collect_findings(
    root: Path,
    today: dt.date,
    check_links: bool,
    timeout: float,
    check_homepage: bool = True,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    projects = root / "_projects"
    for path in sorted(projects.glob("*.md")) if projects.is_dir() else ():
        matter = read_front_matter(path)
        featured = matter.get("featured")
        if featured is None or featured is False:
            continue
        relative = str(path.relative_to(root))
        if featured is not True:
            findings.append(finding("project", relative, "featured must be a boolean"))
        reviewed = parse_date(matter.get("last_reviewed"))
        if reviewed is None:
            findings.append(
                finding(
                    "project",
                    relative,
                    "featured project is missing a valid last_reviewed date",
                )
            )
        elif reviewed > today:
            findings.append(
                finding(
                    "project",
                    relative,
                    f"project review date is in the future ({reviewed})",
                )
            )
        elif (today - reviewed).days > PROJECT_MAX_AGE_DAYS:
            findings.append(
                finding(
                    "project",
                    relative,
                    f"featured project review is older than {PROJECT_MAX_AGE_DAYS} "
                    f"days ({reviewed})",
                )
            )
        for field in ("summary", "outcome"):
            value = matter.get(field)
            if value is None or value == "":
                findings.append(
                    finding("project", relative, f"featured project is missing {field}")
                )
            elif not non_empty_string(value):
                findings.append(
                    finding("project", relative, f"{field} must be a non-empty string")
                )

        has_supported_link = False
        repo = matter.get("repo")
        if repo is not None:
            if not non_empty_string(repo):
                findings.append(
                    finding("link", relative, "repo must be a non-empty string")
                )
            elif not is_http_url(repo):
                findings.append(
                    finding("link", relative, "repo must be an HTTP(S) URL")
                )
            else:
                has_supported_link = True

        demo = matter.get("demo")
        if demo is not None:
            if not non_empty_string(demo):
                findings.append(
                    finding("link", relative, "demo must be a non-empty string")
                )
            elif demo.startswith("/"):
                demo_path = safe_local_path(root, demo)
                if demo_path is None:
                    findings.append(
                        finding("link", relative, f"unsafe local demo path: {demo}")
                    )
                else:
                    has_supported_link = True
                    if not local_target_exists(root, demo, matter.get("permalink")):
                        findings.append(
                            finding(
                                "link",
                                relative,
                                f"local demo does not exist: {demo}",
                            )
                        )
            elif is_http_url(demo):
                has_supported_link = True
            else:
                findings.append(
                    finding(
                        "link",
                        relative,
                        "demo must be HTTP(S) or a root-relative local path",
                    )
                )

        if not has_supported_link:
            findings.append(
                finding(
                    "project",
                    relative,
                    "featured project is missing a valid repo or demo",
                )
            )

        image = matter.get("image")
        if image is None or image == "":
            findings.append(
                finding("project", relative, "featured project is missing image")
            )
        elif not non_empty_string(image):
            findings.append(
                finding("asset", relative, "image must be a non-empty string")
            )
        elif not image.startswith("/"):
            findings.append(
                finding("asset", relative, "image must be a root-relative local path")
            )
        else:
            image_path = safe_local_path(root, image)
            if image_path is None:
                findings.append(
                    finding("asset", relative, f"unsafe local image path: {image}")
                )
            elif not image_path.is_file():
                findings.append(
                    finding("asset", relative, f"project image does not exist: {image}")
                )

        if check_links:
            for field, url in (("repo", repo), ("demo", demo)):
                if isinstance(url, str) and is_http_url(url):
                    available, detail = url_is_available(url, timeout)
                    if not available:
                        findings.append(
                            finding(
                                "link",
                                relative,
                                f"{field} URL is unavailable ({detail}): {url}",
                            )
                        )

    config = parse_config(root / "_config.yml")
    resume_reviewed = parse_date(config.get("resume_last_reviewed"))
    if resume_reviewed is None:
        findings.append(
            finding(
                "resume", "_config.yml", "resume_last_reviewed is missing or invalid"
            )
        )
    elif resume_reviewed > today:
        findings.append(
            finding(
                "resume",
                "_config.yml",
                f"resume review date is in the future ({resume_reviewed})",
            )
        )
    elif (today - resume_reviewed).days > RESUME_MAX_AGE_DAYS:
        findings.append(
            finding(
                "resume",
                "_config.yml",
                f"resume review is older than {RESUME_MAX_AGE_DAYS} "
                f"days ({resume_reviewed})",
            )
        )

    if check_homepage:
        homepage_reviewed = homepage_commit_date(root)
        if homepage_reviewed is None:
            findings.append(
                finding(
                    "homepage",
                    "index.html",
                    "homepage freshness could not be determined from git history",
                )
            )
        elif homepage_reviewed > today:
            findings.append(
                finding(
                    "homepage",
                    "index.html",
                    f"homepage commit date is in the future ({homepage_reviewed})",
                )
            )
        elif (today - homepage_reviewed).days > HOMEPAGE_MAX_AGE_DAYS:
            findings.append(
                finding(
                    "homepage",
                    "index.html",
                    f"homepage has not changed in more than {HOMEPAGE_MAX_AGE_DAYS} "
                    f"days ({homepage_reviewed})",
                )
            )
    return findings


def markdown_report(today: dt.date, findings: list[dict[str, str]]) -> str:
    lines = ["# Portfolio freshness report", "", f"Checked: {today.isoformat()}", ""]
    if not findings:
        return "\n".join(lines + ["No freshness findings.", ""])
    lines.extend((f"Findings: {len(findings)}", ""))
    lines.extend(
        f"- **{item['category']}** `{item['target']}` — {item['message']}"
        for item in findings
    )
    lines.extend(
        (
            "",
            "Resolve the findings and close this issue after the scheduled "
            "check passes.",
            "",
        )
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--today", type=dt.date.fromisoformat, default=dt.datetime.now(dt.UTC).date()
    )
    parser.add_argument("--check-links", action="store_true")
    parser.add_argument(
        "--skip-homepage",
        action="store_true",
        help="Skip the git-history check (for isolated fixtures)",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    findings = collect_findings(
        args.root.resolve(),
        args.today,
        args.check_links,
        args.timeout,
        check_homepage=not args.skip_homepage,
    )
    if args.json:
        report = json.dumps(
            {"checked": args.today.isoformat(), "findings": findings}, indent=2
        )
    else:
        report = markdown_report(args.today, findings)
    if args.output:
        args.output.write_text(
            report + ("" if report.endswith("\n") else "\n"), encoding="utf-8"
        )
    else:
        print(report)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
