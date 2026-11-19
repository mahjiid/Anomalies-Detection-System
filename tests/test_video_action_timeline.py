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

    def test_missing_required_column(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("clip_id,start_time\nclip,00:00.000\n")
            self.assertTrue(any("missing columns" in e for e in validate(path)))


if __name__ == "__main__":
    unittest.main()
