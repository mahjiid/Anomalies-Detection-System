"""Regression tests for malformed Pascal VOC numeric metadata."""
import tempfile
import unittest
from pathlib import Path

from tools.labelimg_voc_to_labelstudio import voc_xml_to_label_studio_task


TEMPLATE = """<annotation>
  <filename>road.jpg</filename>
  <size><width>{width}</width><height>{height}</height></size>
  <object><name>pothole</name><bndbox>
    <xmin>{xmin}</xmin><ymin>10</ymin><xmax>90</xmax><ymax>80</ymax>
  </bndbox></object>
</annotation>"""


class InvalidNumericMetadataTests(unittest.TestCase):
    def convert(self, **overrides):
        fields = dict(width="100", height="100", xmin="5")
        fields.update(overrides)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.xml"
            path.write_text(TEMPLATE.format(**fields), encoding="utf-8")
            return voc_xml_to_label_studio_task(path)

    def test_valid_integer_dimensions_and_rectangle(self):
        task = self.convert()
        result = task["annotations"][0]["result"][0]
        self.assertEqual(result["original_width"], 100)
        self.assertEqual(result["value"]["x"], 5.0)

    def test_rejects_non_finite_dimensions(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "finite"):
                    self.convert(width=value)

    def test_rejects_fractional_dimensions(self):
        with self.assertRaisesRegex(ValueError, "whole pixel"):
            self.convert(height="100.5")

    def test_rejects_non_finite_box_coordinates(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "invalid bounding box"):
                    self.convert(xmin=value)


if __name__ == "__main__":
    unittest.main()
