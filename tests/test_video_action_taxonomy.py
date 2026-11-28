"""Regression tests for project-specific video-action taxonomies."""
import csv
import tempfile
import unittest
from pathlib import Path

from tools.validate_video_action_timeline import REQUIRED, load_taxonomy, validate


class TaxonomyValidationTests(unittest.TestCase):
    def row(self, **overrides):
        row = dict.fromkeys(REQUIRED, "reviewed") | {
            "clip_id": "clip1", "start_time": "00:00.000", "end_time": "00:01.000",
            "actor": "robot", "action": "grasp", "interaction": "contact",
        }
        row.update(overrides)
        return row

    def check_rows(self, rows, taxonomy):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "actions.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=REQUIRED)
                writer.writeheader()
                writer.writerows(rows)
            return validate(path, taxonomy=taxonomy)

    def load(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "taxonomy.json"
            path.write_text(payload, encoding="utf-8")
            return load_taxonomy(path)

    def test_known_taxonomy_values_pass(self):
        taxonomy = {"actor": frozenset({"robot"}), "action": frozenset({"grasp"})}
        self.assertEqual([], self.check_rows([self.row()], taxonomy))

    def test_unknown_value_is_reported_with_source_line(self):
        taxonomy = {"action": frozenset({"grasp", "move"})}
        errors = self.check_rows([self.row(action="lift")], taxonomy)
        self.assertIn(
            "line 2: unknown action value 'lift'; expected one of: grasp, move",
            errors,
        )

    def test_empty_optional_taxonomy_value_is_allowed(self):
        taxonomy = {"interaction": frozenset({"contact", "release"})}
        self.assertEqual([], self.check_rows([self.row(interaction="")], taxonomy))

    def test_loader_rejects_unsupported_field(self):
        with self.assertRaisesRegex(ValueError, "unsupported taxonomy field"):
            self.load('{"end_state": ["held"]}')

    def test_loader_rejects_duplicate_values_after_trimming(self):
        with self.assertRaisesRegex(ValueError, "duplicate taxonomy value"):
            self.load('{"action": ["grasp", " grasp "]}')

    def test_loader_rejects_empty_lists(self):
        with self.assertRaisesRegex(ValueError, "non-empty list"):
            self.load('{"action": []}')

    def test_loader_rejects_invalid_json(self):
        with self.assertRaisesRegex(ValueError, "cannot read taxonomy"):
            self.load("{invalid")


if __name__ == "__main__":
    unittest.main()
