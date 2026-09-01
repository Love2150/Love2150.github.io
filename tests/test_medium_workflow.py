from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "medium-sync.yml"


class MediumWorkflowTests(unittest.TestCase):
    def test_sync_is_daily_reviewable_and_least_privilege(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("cron: '17 11 * * *'", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("pull-requests: write", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("gh auth setup-git", workflow)
        self.assertIn("automation/medium-sync", workflow)
        self.assertIn("gh pr create", workflow)
        self.assertIn("--base main", workflow)
        self.assertIn("--head \"$BRANCH\"", workflow)
        self.assertNotRegex(workflow, r"git push\s*(?:\n|$)")
        self.assertNotIn("git push origin main", workflow)
        self.assertIn("git diff --cached --quiet", workflow)

    def test_sync_uses_pinned_runtime_dependencies_and_actions(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        requirements_path = ROOT / "requirements-medium.txt"
        self.assertTrue(requirements_path.is_file(), "requirements-medium.txt is missing")
        requirements = requirements_path.read_text(encoding="utf-8")

        self.assertIn("python-version: '3.13'", workflow)
        self.assertIn("pip install --require-hashes -r requirements-medium.txt", workflow)
        self.assertRegex(workflow, r"actions/checkout@[0-9a-f]{40}")
        self.assertRegex(workflow, r"actions/setup-python@[0-9a-f]{40}")
        required = {
            "beautifulsoup4",
            "feedparser",
            "markdownify",
            "python-slugify",
            "pytz",
            "requests",
        }
        pinned = {
            line.split("==", 1)[0]
            for line in requirements.splitlines()
            if line and not line.startswith(("#", " ")) and "==" in line
        }
        self.assertTrue(required.issubset(pinned))
        for package in pinned:
            self.assertRegex(
                requirements,
                rf"(?m)^{re.escape(package)}==[^\n]+\\\n\s+--hash=sha256:",
            )


if __name__ == "__main__":
    unittest.main()
