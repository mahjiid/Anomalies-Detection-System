"""Regression tests for invalid numeric Pascal VOC annotation values."""

import tempfile
import unittest
from pathlib import Path

from tools.labelimg_voc_to_labelstudio import voc_xml_to_label_studio_task


class NonFiniteVocValuesTest(unittest.TestCase):
    def convert(self, width="640", height="480", xmin="10", ymin="20", xmax="100", ymax="120"):
        xml = f"""<annotation>
  <filename>road.jpg</filename>
  <size><width>{width}</width><height>{height}</height></size>
  <object><name>Pothole</name><bndbox>
    <xmin>{xmin}</xmin><ymin>{ymin}</ymin><xmax>{xmax}</xmax><ymax>{ymax}</ymax>
  </bndbox></object>
</annotation>"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.xml"
            path.write_text(xml, encoding="utf-8")
            return voc_xml_to_label_studio_task(path)

    def test_valid_box_preserves_percentage_coordinates(self):
        result = self.convert()
        value = result["annotations"][0]["result"][0]["value"]
        self.assertAlmostEqual(value["x"], 1.5625)
        self.assertAlmostEqual(value["y"], 20 / 480 * 100)
        self.assertAlmostEqual(value["width"], 90 / 640 * 100)
        self.assertEqual(value["rectanglelabels"], ["Pothole"])

    def test_nonfinite_image_dimensions_rejected(self):
        for bad in ("nan", "inf", "-inf"):
            with self.subTest(width=bad), self.assertRaises(ValueError):
                self.convert(width=bad)
            with self.subTest(height=bad), self.assertRaises(ValueError):
                self.convert(height=bad)

    def test_nonfinite_box_coordinates_rejected(self):
        for name in ("xmin", "ymin", "xmax", "ymax"):
            for bad in ("nan", "inf", "-inf"):
                with self.subTest(coordinate=name, value=bad), self.assertRaises(ValueError):
                    self.convert(**{name: bad})

    def test_out_of_bounds_and_degenerate_boxes_still_rejected(self):
        for coordinates in (
            {"xmin": "-1"},
            {"xmax": "641"},
            {"xmin": "100", "xmax": "100"},
            {"ymin": "120", "ymax": "120"},
        ):
            with self.subTest(coordinates=coordinates), self.assertRaises(ValueError):
                self.convert(**coordinates)


if __name__ == "__main__":
    unittest.main()
