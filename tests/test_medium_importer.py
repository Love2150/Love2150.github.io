from __future__ import annotations

import importlib.util
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "medium_to_jekyll", ROOT / "scripts" / "medium_to_jekyll.py"
)
assert SPEC and SPEC.loader
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


class Entry(dict):
    def __getattr__(self, name: str):
        return self[name]


def sample_entry() -> Entry:
    published = time.strptime("2026-08-30 12:00:00", "%Y-%m-%d %H:%M:%S")
    return Entry(
        title="Investigating Suspicious PowerShell",
        link="https://medium.com/@brandonlove2150/investigating-powershell-123",
        published_parsed=published,
        tags=[{"term": "DFIR"}],
        content=[
            {
                "value": """
                <h3>Investigation Walkthrough</h3>
                <p>A suspicious PowerShell alert led to a focused endpoint investigation. The evidence showed an encoded download attempt.</p>
                <figure>
                  <img src="https://cdn-images.medium.com/evidence.png" alt="">
                  <figcaption>PowerShell process tree showing the encoded command</figcaption>
                </figure>
                <img src="https://cdn-images.medium.com/uncaptioned.png" alt="">
                <img src="https://Medium.com/_/stat?event=post.clientViewed" alt="">
                """
            }
        ],
    )


class MediumImporterTests(unittest.TestCase):
    def test_new_post_has_summary_canonical_and_descriptive_image_alt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = IMPORTER.write_post(directory, "Brandon Love", sample_entry())
            self.assertIsNotNone(path)
            text = Path(path).read_text(encoding="utf-8")

        self.assertIn(
            'summary: "A suspicious PowerShell alert led to a focused endpoint investigation."',
            text,
        )
        self.assertIn(
            'canonical_url: "https://medium.com/@brandonlove2150/investigating-powershell-123"',
            text,
        )
        self.assertIn("date: 2026-08-30 07:00:00 -0500", text)
        self.assertIn(
            "![PowerShell process tree showing the encoded command]"
            "(https://cdn-images.medium.com/evidence.png)",
            text,
        )
        self.assertIn(
            "![Investigating Suspicious PowerShell evidence image]"
            "(https://cdn-images.medium.com/uncaptioned.png)",
            text,
        )
        self.assertNotIn("medium.com/_/stat", text.lower())

    def test_yaml_scalar_escapes_windows_paths_and_control_characters(self) -> None:
        self.assertEqual('"C:\\\\Windows\\\\Temp\\nalert"', IMPORTER.yq("C:\\Windows\\Temp\nalert"))

    def test_summary_removes_markdown_link_syntax(self) -> None:
        summary = IMPORTER.summary_from_markdown(
            "This is a sufficiently long paragraph with a [linked source](https://example.com) for review."
        )
        self.assertEqual(
            "This is a sufficiently long paragraph with a linked source for review.",
            summary,
        )

    def test_same_title_and_date_use_canonical_url_to_avoid_collisions(self) -> None:
        first_entry = sample_entry()
        second_entry = sample_entry()
        second_entry["link"] = "https://medium.com/@brandonlove2150/investigating-powershell-456"

        with tempfile.TemporaryDirectory() as directory:
            first = IMPORTER.write_post(directory, "Brandon Love", first_entry)
            second = IMPORTER.write_post(directory, "Brandon Love", second_entry)
            second_rerun = IMPORTER.write_post(directory, "Brandon Love", second_entry)
            files = sorted(Path(directory).glob("*.md"))

        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertIsNone(second_rerun)
        self.assertEqual(2, len(files))
        self.assertNotEqual(Path(first).name, Path(second).name)

    def test_summary_starts_at_the_beginning_of_a_long_sentence(self) -> None:
        sentence = (
            "This investigation begins with important evidence "
            + ("and context " * 30)
            + ". Next sentence."
        )
        self.assertTrue(IMPORTER.first_sentence(sentence).startswith("This investigation"))

    def test_rerun_is_idempotent_and_reports_no_new_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = IMPORTER.write_post(directory, "Brandon Love", sample_entry())
            self.assertIsNotNone(first)
            original = Path(first).read_text(encoding="utf-8")

            second = IMPORTER.write_post(directory, "Brandon Love", sample_entry())

            self.assertIsNone(second)
            self.assertEqual(original, Path(first).read_text(encoding="utf-8"))
            self.assertEqual(1, len(list(Path(directory).glob("*.md"))))


if __name__ == "__main__":
    unittest.main()
