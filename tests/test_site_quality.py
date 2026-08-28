from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".html", ".md", ".yml", ".yaml", ".scss", ".css", ".js", ".mjs"}


def body_without_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


class SiteQualityTests(unittest.TestCase):
    def test_source_contains_no_forbidden_c1_control_characters(self) -> None:
        failures: list[str] = []
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8")
            controls = sorted({f"U+{ord(char):04X}" for char in text if 0x80 <= ord(char) <= 0x9F})
            if controls:
                failures.append(f"{path.relative_to(ROOT)}: {', '.join(controls)}")
        self.assertEqual([], failures)

    def test_required_brand_and_resume_assets_exist(self) -> None:
        required = [
            ROOT / "favicon.svg",
            ROOT / "favicon.ico",
            ROOT / "assets/images/brand/brandmark.svg",
            ROOT / "assets/images/brand/brandmark.png",
            ROOT / "assets/Brandon_Love_Cybersecurity_Resume.pdf",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_homepage_links_favicon_and_pdf_resume(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('rel="icon"', homepage)
        self.assertIn("Brandon_Love_Cybersecurity_Resume.pdf", homepage)
        self.assertIn("Download Resume (PDF)", homepage)
        self.assertIn("Resume (DOCX)", homepage)

    def test_project_markdown_does_not_duplicate_layout_h1(self) -> None:
        failures: list[str] = []
        for path in sorted((ROOT / "_projects").glob("*.md")):
            body = body_without_front_matter(path.read_text(encoding="utf-8"))
            headings: list[str] = []
            inside_fence = False
            for line in body.splitlines():
                if line.startswith("```"):
                    inside_fence = not inside_fence
                    continue
                if not inside_fence and re.match(r"^#\s+", line):
                    headings.append(line)
            if headings:
                failures.append(f"{path.name}: {headings}")
        self.assertEqual([], failures)

    def test_markdown_code_fences_are_balanced(self) -> None:
        failures: list[str] = []
        for folder in (ROOT / "_projects", ROOT / "_posts", ROOT / "reports/analyst_report"):
            for path in sorted(folder.glob("*.md")):
                count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("```"))
                if count % 2:
                    failures.append(f"{path.relative_to(ROOT)}: {count} fences")
        self.assertEqual([], failures)

    def test_post_layout_has_one_closing_html_tag(self) -> None:
        layout = (ROOT / "_layouts/post.html").read_text(encoding="utf-8")
        self.assertEqual(1, layout.lower().count("</html>"))

    def test_carousel_controls_are_exposed_and_touch_sized(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        for class_name in ("proj-nav", "proj-dots", "blog-nav", "blog-dots"):
            pattern = rf'class="{class_name}"[^>]*aria-hidden="true"'
            self.assertIsNone(re.search(pattern, homepage), class_name)
        self.assertRegex(homepage, r"\.blog-btn,[\s\S]*?min-width:\s*44px")
        self.assertRegex(homepage, r"\.blog-dot,[\s\S]*?min-width:\s*44px")

    def test_accessible_names_include_visible_text(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('class="brand" href="{{ \'/\' | relative_url }}" aria-label="Home"', homepage)
        self.assertNotRegex(homepage, r'<span class="btn-contact"\s+aria-label=')

    def test_light_mode_defines_a_high_contrast_accent(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        light_mode = re.search(r"@media \(prefers-color-scheme: light\) \{([\s\S]*?)\n    \}", homepage)
        self.assertIsNotNone(light_mode)
        assert light_mode is not None
        self.assertIn("--accent: #2563eb;", light_mode.group(1))

    def test_hero_preserves_page_gutters(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        hero_grid = re.search(r"\.hero-grid\s*\{([\s\S]*?)\}", homepage)
        self.assertIsNotNone(hero_grid)
        assert hero_grid is not None
        self.assertNotRegex(hero_grid.group(1), r"width:\s*100%")

    def test_skill_pills_use_readable_text_color(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        skill_pill = re.search(r"\.skill-pill\s*\{([\s\S]*?)\}", homepage)
        self.assertIsNotNone(skill_pill)
        assert skill_pill is not None
        self.assertIn("color: var(--text);", skill_pill.group(1))
        self.assertIn("background: rgba(37, 99, 235, .08);", skill_pill.group(1))

    def test_mobile_role_labels_do_not_use_orphanable_pipes(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("SOC Analyst | Incident Response | Detection Engineering", homepage)
        self.assertIn('class="hero-role-item"', homepage)


if __name__ == "__main__":
    unittest.main()
