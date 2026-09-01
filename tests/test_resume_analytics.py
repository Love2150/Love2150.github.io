from __future__ import annotations

import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ResumeAnalyticsTests(unittest.TestCase):
    def test_cloudflare_web_analytics_is_enabled_with_site_token(self) -> None:
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        match = re.search(
            r'^cloudflare_analytics_token:\s*"([0-9a-f]{32})"$', config, re.MULTILINE
        )
        self.assertIsNotNone(match)
        include = (ROOT / "_includes/analytics.html").read_text(encoding="utf-8")
        self.assertIn('type="module"', include)
        self.assertIn("https://static.cloudflareinsights.com/beacon.min.js", include)
        self.assertIn("site.cloudflare_analytics_token", include)

    def test_resume_reports_twelve_plus_years(self) -> None:
        document = ROOT / "assets/Brandon_Love_Cybersecurity_Resume.docx"
        with zipfile.ZipFile(document) as archive:
            xml = archive.read("word/document.xml").decode("utf-8")
        self.assertIn("12+ years", xml)
        self.assertNotIn("10 years", xml)
        self.assertGreater(
            (ROOT / "assets/Brandon_Love_Cybersecurity_Resume.pdf").stat().st_size, 0
        )

    def test_resume_has_no_hidden_organizational_or_tracking_metadata(self) -> None:
        document = ROOT / "assets/Brandon_Love_Cybersecurity_Resume.docx"
        with zipfile.ZipFile(document) as archive:
            package_text = "\n".join(
                archive.read(name).decode("utf-8", "ignore")
                for name in archive.namelist()
                if name.endswith((".xml", ".rels"))
            )
        for forbidden in (
            "SSG USARMY",
            "416 ENG CMD",
            "GrammarlyDocumentId",
            "classificationlabels",
            "mipLabelMetadata",
            "MSIP_Label",
        ):
            self.assertNotIn(forbidden, package_text)

    def test_resume_review_date_is_current(self) -> None:
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r"(?m)^resume_last_reviewed:\s*2026-09-01$")


if __name__ == "__main__":
    unittest.main()
