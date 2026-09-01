from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_freshness.py"


class PhaseFiveAutomationTests(unittest.TestCase):
    def run_checker(
        self, root: Path, today: str = "2026-09-01", *, skip_homepage: bool = True
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root),
            "--today",
            today,
            "--json",
        ]
        if skip_homepage:
            command.append("--skip-homepage")
        return subprocess.run(  # noqa: S603 - command uses the current Python and fixed checker
            command,
            check=False,
            capture_output=True,
            text=True,
        )

    def make_site(
        self, project_front_matter: str, *, resume_reviewed: str = "2026-08-01"
    ) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "_projects").mkdir()
        (root / "assets").mkdir()
        (root / "_projects" / "example.md").write_text(
            f"---\n{project_front_matter}\n---\nEvidence.\n", encoding="utf-8"
        )
        (root / "_config.yml").write_text(
            f"resume_last_reviewed: {resume_reviewed}\n", encoding="utf-8"
        )
        (root / "assets" / "resume.pdf").write_bytes(b"%PDF")
        return root

    def test_freshness_checker_accepts_complete_current_featured_project(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    'summary: "What the project demonstrates."',
                    'outcome: "A verified result."',
                    "image: /assets/example.png",
                    "repo: https://github.com/example/example",
                )
            )
        )
        (root / "assets" / "example.png").write_bytes(b"png")

        result = self.run_checker(root)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], json.loads(result.stdout)["findings"])

    def test_freshness_checker_reports_stale_and_incomplete_featured_project(
        self,
    ) -> None:
        root = self.make_site(
            "\n".join(("title: Example", "featured: true", "last_reviewed: 2026-01-01"))
        )

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        findings = json.loads(result.stdout)["findings"]
        messages = "\n".join(item["message"] for item in findings)
        self.assertIn("older than 90 days", messages)
        for field in ("summary", "outcome", "image", "repo or demo"):
            self.assertIn(field, messages)

    def test_freshness_checker_reports_missing_internal_demo(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    'summary: "What the project demonstrates."',
                    'outcome: "A verified result."',
                    "image: /assets/example.png",
                    "demo: /reports/missing.html",
                )
            )
        )
        (root / "assets" / "example.png").write_bytes(b"png")

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("local demo does not exist", messages)

    def test_freshness_checker_rejects_local_path_traversal(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    'summary: "What the project demonstrates."',
                    'outcome: "A verified result."',
                    "image: /../../etc/passwd",
                    "demo: /../../etc/passwd",
                )
            )
        )
        (root / "assets" / "example.png").write_bytes(b"png")

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("unsafe local demo path", messages)
        self.assertIn("unsafe local image path", messages)

    def test_freshness_checker_rejects_truthy_non_boolean_featured_value(self) -> None:
        root = self.make_site('title: Example\nfeatured: "false"')

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = self.finding_messages(result)
        self.assertIn("featured must be a boolean", messages)
        self.assertIn("featured project is missing summary", messages)

    def test_freshness_checker_rejects_relative_metadata_paths(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    'summary: "What the project demonstrates."',
                    'outcome: "A verified result."',
                    "image: ../../etc/passwd",
                    "demo: ../../etc/passwd",
                )
            )
        )

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = self.finding_messages(result)
        self.assertIn("image must be a root-relative local path", messages)
        self.assertIn("demo must be HTTP(S) or a root-relative local path", messages)

    def test_freshness_checker_rejects_unsafe_url_schemes(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    'summary: "What the project demonstrates."',
                    'outcome: "A verified result."',
                    "image: /assets/example.png",
                    "repo: javascript:alert(1)",
                )
            )
        )
        (root / "assets" / "example.png").write_bytes(b"png")

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        self.assertIn("repo must be an HTTP(S) URL", self.finding_messages(result))

    def test_freshness_checker_rejects_non_string_metadata(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true",
                    "last_reviewed: 2026-08-15",
                    "summary: {text: nope}",
                    "outcome: [not, text]",
                    "image: true",
                    "repo: true",
                )
            )
        )

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = self.finding_messages(result)
        for field in ("summary", "outcome", "image", "repo"):
            self.assertIn(f"{field} must be a non-empty string", messages)

    def test_freshness_checker_reports_future_review_dates(self) -> None:
        root = self.make_site(
            "\n".join(
                ("title: Example", "featured: true", "last_reviewed: 2027-01-01")
            ),
            resume_reviewed="2027-01-01",
        )

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("project review date is in the future", messages)
        self.assertIn("resume review date is in the future", messages)

    def test_freshness_checker_parses_yaml_comments_and_colons(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: true # recruiter-facing case study",
                    "last_reviewed: 2026-08-15",
                    'outcome: "Result: passed"',
                    "image: /assets/example.png",
                    "repo: https://github.com/example/example",
                )
            )
        )
        (root / "assets" / "example.png").write_bytes(b"png")

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("featured project is missing summary", messages)

    def test_freshness_checker_reports_stale_resume_review_date(self) -> None:
        root = self.make_site(
            "\n".join(
                (
                    "title: Example",
                    "featured: false",
                    "last_reviewed: 2026-08-15",
                )
            ),
            resume_reviewed="2025-01-01",
        )

        result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("resume review is older than 183 days", messages)

    @staticmethod
    def finding_messages(result: subprocess.CompletedProcess[str]) -> str:
        return "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )

    def test_current_portfolio_has_no_freshness_findings(self) -> None:
        result = self.run_checker(ROOT, skip_homepage=False)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_freshness_checker_fails_closed_without_homepage_history(self) -> None:
        root = self.make_site("title: Example\nfeatured: false")

        result = self.run_checker(root, skip_homepage=False)

        self.assertEqual(1, result.returncode)
        messages = "\n".join(
            item["message"] for item in json.loads(result.stdout)["findings"]
        )
        self.assertIn("homepage freshness could not be determined", messages)

    def test_repository_defines_quality_freshness_and_dependency_automation(
        self,
    ) -> None:
        quality = (ROOT / ".github/workflows/quality-gates.yml").read_text(
            encoding="utf-8"
        )
        freshness = (ROOT / ".github/workflows/freshness.yml").read_text(
            encoding="utf-8"
        )
        dependabot = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")

        for command in (
            "python -m pip install --require-hashes -r requirements-medium.txt",
            "python -m pip install --require-hashes -r requirements-quality.txt",
            "python -m unittest discover",
            "bundle exec jekyll build",
            "bundle exec htmlproofer",
            "treosh/lighthouse-ci-action@",
            "configPath: lighthouserc.json",
        ):
            self.assertIn(command, quality)
        self.assertIn("pull_request:", quality)
        self.assertIn("contents: read", quality)
        self.assertNotIn("--config-file", quality)
        self.assertNotIn("--no-ignore-empty-alt", quality)
        self.assertIn("--disable-external --no-enforce-https", quality)
        self.assertFalse((ROOT / ".htmlproofer.yml").exists())
        self.assertIn("scripts/check_freshness.py", freshness)
        self.assertIn("requirements-quality.txt", freshness)
        self.assertIn("issues: write", freshness)
        for ecosystem in ("bundler", "github-actions", "pip"):
            self.assertIn(f'package-ecosystem: "{ecosystem}"', dependabot)
        self.assertNotIn('package-ecosystem: "npm"', dependabot)

    def test_unused_cyber_tips_pipeline_is_removed(self) -> None:
        removed = (
            ROOT / ".github/workflows/update-tips.yml",
            ROOT / "scripts/fetch-feeds.mjs",
            ROOT / "assets/tips.json",
        )
        self.assertEqual(
            [], [str(path.relative_to(ROOT)) for path in removed if path.exists()]
        )
        self.assertFalse((ROOT / "package.json").exists())
        self.assertFalse((ROOT / "package-lock.json").exists())


if __name__ == "__main__":
    unittest.main()
