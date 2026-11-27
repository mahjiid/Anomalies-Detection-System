"""Regression tests for video-action timeline metadata validation."""
import csv
import tempfile
import unittest
from pathlib import Path

from tools.validate_video_action_timeline import REQUIRED, seconds, validate


class TimelineValidationTests(unittest.TestCase):
    def check_rows(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "actions.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=REQUIRED)
                writer.writeheader()
                writer.writerows(rows)
            return validate(path)

    def row(self, clip="clip1", start="00:00.000", end="00:01.000"):
        return dict.fromkeys(REQUIRED, "reviewed") | {
            "clip_id": clip, "start_time": start, "end_time": end,
            "actor": "robot", "action": "grasp"
        }

    def test_adjacent_segments_valid(self):
        self.assertEqual([], self.check_rows([
            self.row(end="00:01.000"),
            self.row(start="00:01.000", end="00:02.000")]))

    def test_overlap_detected_even_when_rows_unsorted(self):
        errors = self.check_rows([
            self.row(start="00:01.000", end="00:03.000"),
            self.row(start="00:00.000", end="00:02.000")])
        self.assertTrue(any("overlapping" in error for error in errors))

    def test_nested_intervals_detected(self):
        # The first segment contains both later segments. A check comparing
        # only consecutive intervals would miss the first-versus-third overlap.
        errors = self.check_rows([
            self.row(start="00:00.000", end="00:10.000"),
            self.row(start="00:01.000", end="00:02.000"),
            self.row(start="00:03.000", end="00:04.000"),
        ])
        self.assertTrue(any("lines 2 and 4" in error for error in errors), errors)

    def test_different_clips_can_overlap(self):
        self.assertEqual([], self.check_rows([self.row(), self.row(clip="clip2")]))

    def test_zero_duration_rejected(self):
        self.assertTrue(any("must exceed" in error for error in self.check_rows([
            self.row(end="00:00.000")])))

    def test_invalid_seconds_rejected(self):
        self.assertTrue(any("invalid timestamp" in error for error in self.check_rows([
            self.row(end="00:61.000")])))

    def test_hours_format(self):
        self.assertEqual(3601.25, seconds("01:00:01.250"))

    def test_duplicate_column_headers_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "duplicate.csv"
            path.write_text(",".join(REQUIRED + ("clip_id",)) + "\n")
            self.assertTrue(any("duplicate columns: clip_id" in e for e in validate(path)))

    def test_missing_required_column(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.csv"
            path.write_text("clip_id,start_time\nclip,00:00.000\n")
            self.assertTrue(any("missing columns" in e for e in validate(path)))

    def test_error_line_uses_physical_line_after_multiline_field(self):
        first = self.row()
        first["reviewer_note"] = "first line\nsecond line"
        second = self.row(start="00:01.000", end="00:02.000")
        second["actor"] = ""

        errors = self.check_rows([first, second])

        # Header is line 1; the first record spans lines 2-3; the second
        # record therefore starts and ends on physical line 4.
        self.assertIn("line 4: empty actor", errors)

    def test_unterminated_quoted_field_is_rejected_with_physical_line(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "malformed.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream)
                writer.writerow(REQUIRED)
                first = self.row()
                first["reviewer_note"] = "first line\nsecond line"
                writer.writerow([first[name] for name in REQUIRED])
                stream.write(
                    'clip2,00:01.000,00:02.000,robot,move,block,none,moved,'
                    'complete,high,"unfinished\n'
                )

            errors = validate(path)

            self.assertTrue(
                any("line 4: malformed CSV:" in error for error in errors),
                errors,
            )

    def test_malformed_header_is_reported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "malformed-header.csv"
            path.write_text('"clip_id,start_time\n', encoding="utf-8")

            errors = validate(path)

            self.assertTrue(
                any("line 1: malformed CSV:" in error for error in errors),
                errors,
            )

    def test_short_record_rejects_omitted_trailing_cells(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "short-row.csv"
            path.write_text(
                ",".join(REQUIRED) + "\n"
                "clip1,00:00.000,00:01.000,robot,grasp,block,contact,held,aligned\n",
                encoding="utf-8",
            )

            errors = validate(path)

            self.assertIn(
                "line 2: missing CSV values: confidence, reviewer_note",
                errors,
            )

    def test_explicitly_empty_optional_cells_are_allowed(self):
        row = self.row()
        for name in ("object", "interaction", "end_state", "instruction_alignment", "confidence", "reviewer_note"):
            row[name] = ""

        self.assertEqual([], self.check_rows([row]))


if __name__ == "__main__":
    unittest.main()
