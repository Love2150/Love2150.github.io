from __future__ import annotations

import re
import struct
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class PhaseSixSeoTests(unittest.TestCase):
    def test_site_has_complete_identity_and_social_metadata(self) -> None:
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        for field in (
            "title:",
            "description:",
            "author:",
            "locale:",
            "logo:",
            "social:",
        ):
            self.assertIn(field, config)
        self.assertIn("Brandon Love", config)
        self.assertIn("https://github.com/Love2150", config)
        self.assertIn("https://www.linkedin.com/in/brandon-love-85b247261", config)
        parsed = yaml.safe_load(config)
        self.assertEqual(
            "/assets/images/og-default.png", parsed["defaults"][0]["values"]["image"]
        )

    def test_default_layout_emits_structured_data_and_optional_analytics(self) -> None:
        layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertIn("{% include structured-data.html %}", layout)
        self.assertIn("{% include analytics.html %}", layout)
        analytics = (ROOT / "_includes/analytics.html").read_text(encoding="utf-8")
        self.assertIn("site.cloudflare_analytics_token", analytics)
        self.assertIn("data-cf-beacon", analytics)
        self.assertIn('type="module"', analytics)

    def test_structured_data_covers_person_profile_and_projects(self) -> None:
        structured = (ROOT / "_includes/structured-data.html").read_text(
            encoding="utf-8"
        )
        for schema_type in ("Person", "ProfilePage", "CreativeWork"):
            self.assertIn(schema_type, structured)
        self.assertIn(
            "page.og_image | default: page.image | default: site.image", structured
        )
        self.assertIn("jsonify", structured)
        self.assertIn("site.social.links", structured)

    def test_homepage_and_contact_page_state_recruiter_conversion_details(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        contact = (ROOT / "contact/index.html").read_text(encoding="utf-8")
        combined = homepage + contact
        for phrase in (
            "Open to SOC, incident response, and detection engineering roles",
            "Killeen, Texas",
            "remote and on-site opportunities",
            "Download Resume (PDF)",
        ):
            self.assertIn(phrase, combined)
        self.assertIn("layout: default", contact)
        self.assertIn("brandonlove2150@icloud.com", contact)
        self.assertNotIn("Resume (DOCX)", homepage)

    def test_featured_projects_have_social_images_and_descriptions(self) -> None:
        failures: list[str] = []
        for path in sorted((ROOT / "_projects").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            matter_match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
            if not matter_match or not re.search(
                r"(?m)^featured:\s*true\s*$", matter_match.group(1)
            ):
                continue
            matter = matter_match.group(1)
            if not re.search(r"(?m)^(?:og_image|image):\s*\S+", matter):
                failures.append(f"{path.name}: social image")
            if not re.search(r"(?m)^(?:summary|description):\s*.+", matter):
                failures.append(f"{path.name}: description")
        self.assertEqual([], failures)

    def test_default_social_image_is_open_graph_sized_png(self) -> None:
        image = ROOT / "assets/images/og-default.png"
        data = image.read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", data[:8])
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((1200, 630), (width, height))


if __name__ == "__main__":
    unittest.main()
