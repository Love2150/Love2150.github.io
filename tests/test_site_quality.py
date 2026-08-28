from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".html", ".md", ".yml", ".yaml", ".scss", ".css", ".js", ".mjs"}
FLAGSHIPS = (
    "sentinal-defender-lab.md",
    "winlog-triage.md",
    "pcap-quick-profiler.md",
)


def body_without_front_matter(text: str) -> str:
    match = re.match(r"\A---\n.*?\n---\n", text, re.DOTALL)
    return text[match.end():] if match else text


def front_matter(text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else ""


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
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

    def test_shared_visual_system_files_and_versioned_stylesheet_exist(self) -> None:
        required = [
            ROOT / "_layouts/default.html",
            ROOT / "_layouts/project.html",
            ROOT / "_layouts/post.html",
            ROOT / "_layouts/report.html",
            ROOT / "_includes/header.html",
            ROOT / "_includes/footer.html",
            ROOT / "assets/css/style.scss",
        ]
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])
        default = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertIn("{% include header.html %}", default)
        self.assertIn("{% include footer.html %}", default)
        self.assertRegex(default, r"assets/css/style\.css' \| relative_url }}\?v=")

    def test_default_layout_has_one_metadata_source_and_loads_declared_fonts(self) -> None:
        default = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertNotIn("<title>", default)
        self.assertNotIn('<meta name="description"', default)
        self.assertEqual(1, default.count("{% seo %}"))
        self.assertIn("fonts.googleapis.com", default)
        self.assertIn("IBM+Plex+Mono", default)
        self.assertIn("IBM+Plex+Sans", default)

    def test_medium_posts_preserve_medium_as_canonical_url(self) -> None:
        failures: list[str] = []
        for path in sorted((ROOT / "_posts").glob("*.md")):
            matter = front_matter(path.read_text(encoding="utf-8"))
            medium = re.search(r'^medium_canonical:\s*["\']?([^"\'\n]+)', matter, re.MULTILINE)
            if not medium:
                continue
            canonical = re.search(r'^canonical_url:\s*["\']?([^"\'\n]+)', matter, re.MULTILINE)
            if not canonical or canonical.group(1) != medium.group(1):
                failures.append(path.name)
        self.assertEqual([], failures)
        importer = (ROOT / "scripts/medium_to_jekyll.py").read_text(encoding="utf-8")
        self.assertIn("canonical_url:", importer)
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r"(?m)^url:\s*https://love2150\.github\.io\s*$")

    def test_primary_pages_use_shared_layouts(self) -> None:
        expected = {
            "index.html": "default",
            "projects/index.html": "default",
            "archive/index.html": "default",
            "medium.html": "default",
            "reports/analyst_report/index.html": "report",
        }
        failures = []
        for relative, layout in expected.items():
            matter = front_matter((ROOT / relative).read_text(encoding="utf-8"))
            if not re.search(rf"^layout:\s*{layout}\s*$", matter, re.MULTILINE):
                failures.append(f"{relative}: expected {layout}")
        self.assertEqual([], failures)
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r'type:\s*"projects"[\s\S]*?layout:\s*project')
        self.assertRegex(config, r'path:\s*"reports/analyst_report"[\s\S]*?layout:\s*report')

    def test_homepage_has_exactly_three_evidence_based_flagship_cards(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Selected Security Work", homepage)
        self.assertNotIn("Portfolio Highlights", homepage)
        self.assertNotIn("Featured Projects", homepage)
        cards = re.findall(r'<article class="case-card flagship-card"[\s\S]*?</article>', homepage)
        self.assertEqual(3, len(cards))
        joined = "\n".join(cards)
        for title in ("Microsoft Sentinel + Defender", "Windows Log Triage", "PCAP Quick Profiler"):
            self.assertIn(title, joined)
        for label in ("Problem", "Built", "Validation", "Outcome"):
            self.assertEqual(3, len(re.findall(rf">\s*{label}\s*<", joined)))

    def test_flagships_have_truthful_review_metadata_and_project_layout(self) -> None:
        required_keys = ("status", "featured", "last_reviewed", "role", "tools", "outcome")
        failures: list[str] = []
        for filename in FLAGSHIPS:
            matter = front_matter((ROOT / "_projects" / filename).read_text(encoding="utf-8"))
            if not re.search(r"^layout:\s*project\s*$", matter, re.MULTILINE):
                failures.append(f"{filename}: layout")
            for key in required_keys:
                if not re.search(rf"^{key}:\s*.+$", matter, re.MULTILINE):
                    failures.append(f"{filename}: {key}")
            if not re.search(r"^featured:\s*true\s*$", matter, re.MULTILINE):
                failures.append(f"{filename}: featured true")
            if not re.search(r"^last_reviewed:\s*2026-08-28\s*$", matter, re.MULTILINE):
                failures.append(f"{filename}: review date")
        self.assertEqual([], failures)

    def test_sentinel_summary_matches_visible_evidence(self) -> None:
        project = (ROOT / "_projects/sentinal-defender-lab.md").read_text(encoding="utf-8")
        matter = front_matter(project)
        self.assertIn('status: "Documented lab"', matter)
        self.assertIn('outcome_label: "Documented result"', matter)
        self.assertNotIn("wrote playbook enrichment back to the incident", project.lower())
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("wrote enrichment back to the incident", homepage.lower())
        layout = (ROOT / "_layouts/project.html").read_text(encoding="utf-8")
        self.assertIn('page.outcome_label | default: "Verified outcome"', layout)

    def test_project_proof_strip_orders_two_column_fields_before_full_outcome(self) -> None:
        layout = (ROOT / "_layouts/project.html").read_text(encoding="utf-8")
        self.assertLess(layout.index("Last reviewed"), layout.index("Verified outcome"))
        css = (ROOT / "assets/css/style.scss").read_text(encoding="utf-8")
        self.assertIn(".operation-card { align-self: start;", css)
        self.assertIn("object-position: center 62%;", css)
        self.assertIn(".report-card-thumb { aspect-ratio: 16 / 9; }", css)
        self.assertIn(".report-card-thumb img { object-fit: cover;", css)

    def test_project_layout_exposes_recruiter_proof_strip_and_evidence_labels(self) -> None:
        layout = (ROOT / "_layouts/project.html").read_text(encoding="utf-8")
        self.assertIn('{% if page.status or page.role or page.tools or page.outcome or page.last_reviewed %}', layout)
        self.assertIn('class="proof-strip"', layout)
        for label in ("Status", "Role", "Tools", "Verified outcome", "Last reviewed"):
            self.assertIn(label, layout)
        self.assertIn("{{ content }}", layout)

    def test_report_index_uses_real_images_or_deliberate_text_treatment(self) -> None:
        index = (ROOT / "reports/analyst_report/index.html").read_text(encoding="utf-8")
        self.assertNotIn("fallback.jpg", index)
        self.assertIn("{% if r.image %}", index)
        self.assertIn('class="report-card-evidence"', index)
        self.assertIn("Evidence brief", index)

    def test_report_thumbnails_fill_cards_without_prose_margins(self) -> None:
        css = (ROOT / "assets/css/style.scss").read_text(encoding="utf-8")
        self.assertIn(".report-card-thumb { aspect-ratio: 16 / 9; }", css)
        self.assertIn(".report-card-thumb img { object-fit: cover;", css)
        self.assertIn(".prose > img {", css)
        self.assertNotRegex(css, r"\.prose\s+img\s*\{")

    def test_role_labels_wrap_without_orphaned_separators(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(3, homepage.count('class="hero-role-item"'))
        self.assertNotIn("SOC Analyst · Incident Response · Detection Engineering", homepage)
        css = (ROOT / "assets/css/style.scss").read_text(encoding="utf-8")
        self.assertIn(".hero-role-item + .hero-role-item::before", css)
        self.assertIn('content: "·";', css)
        self.assertIn("white-space: nowrap;", css)
        self.assertRegex(css, r"@media \(max-width: 640px\)[\s\S]*?\.hero-role-item \+ \.hero-role-item::before \{ content: none; \}")

    def test_shared_navigation_marks_current_section(self) -> None:
        header = (ROOT / "_includes/header.html").read_text(encoding="utf-8")
        self.assertIn('aria-current="page"', header)
        self.assertIn("page.collection == 'projects'", header)
        self.assertIn("page.url contains '/reports/'", header)
        css = (ROOT / "assets/css/style.scss").read_text(encoding="utf-8")
        self.assertIn('[aria-current="page"]', css)

    def test_shared_css_meets_visual_and_accessibility_contract(self) -> None:
        css = (ROOT / "assets/css/style.scss").read_text(encoding="utf-8")
        for token in ("IBM Plex Sans", "IBM Plex Mono", "--space-1: 8px", "--gutter: 32px", "#07111f"):
            self.assertIn(token, css)
        self.assertRegex(css, r"@media\s*\(max-width:\s*640px\)[\s\S]*?--gutter:\s*16px")
        self.assertIn(":focus-visible", css)
        self.assertRegex(css, r"min-(?:height|block-size):\s*44px")
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("width: calc(100% - (var(--gutter) * 2));", css)
        self.assertIn("max-width: var(--max-width);", css)
        self.assertNotIn("linear-gradient", css)
        self.assertNotIn("radial-gradient", css)

    def test_mobile_navigation_has_no_hidden_focusable_links(self) -> None:
        header = (ROOT / "_includes/header.html").read_text(encoding="utf-8")
        self.assertIn("<details", header)
        self.assertIn("<summary", header)
        self.assertNotIn("display: none", header)
        self.assertIn('aria-label="Primary navigation"', header)

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

    def test_homepage_preserves_favicon_and_resume_links(self) -> None:
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Brandon_Love_Cybersecurity_Resume.pdf", homepage)
        self.assertIn("Download Resume (PDF)", homepage)
        default = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        self.assertIn('rel="icon"', default)
        self.assertIn("favicon.ico", default)


if __name__ == "__main__":
    unittest.main()
