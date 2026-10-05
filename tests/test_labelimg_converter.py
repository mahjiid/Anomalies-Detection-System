import tempfile
import unittest
from pathlib import Path

from tools.labelimg_voc_to_labelstudio import voc_xml_to_label_studio_task


SAMPLE_XML = """<annotation>
  <filename>road_001.jpg</filename>
  <size>
    <width>640</width>
    <height>480</height>
    <depth>3</depth>
  </size>
  <object>
    <name>pothole</name>
    <bndbox>
      <xmin>64</xmin>
      <ymin>96</ymin>
      <xmax>320</xmax>
      <ymax>240</ymax>
    </bndbox>
  </object>
</annotation>
"""


class LabelImgConverterTests(unittest.TestCase):
    def test_converts_voc_box_to_label_studio_percentages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "road_001.xml"
            xml_path.write_text(SAMPLE_XML, encoding="utf-8")

            task = voc_xml_to_label_studio_task(
                xml_path,
                image_prefix="/data/local-files/?d=images",
            )

            result = task["annotations"][0]["result"][0]
            self.assertEqual(task["data"]["image"], "/data/local-files/?d=images/road_001.jpg")
            self.assertEqual(result["value"]["rectanglelabels"], ["pothole"])
            self.assertEqual(result["value"]["x"], 10.0)
            self.assertEqual(result["value"]["y"], 20.0)
            self.assertEqual(result["value"]["width"], 40.0)
            self.assertEqual(result["value"]["height"], 30.0)

    def test_rejects_out_of_bounds_box(self):
        invalid = SAMPLE_XML.replace("<xmax>320</xmax>", "<xmax>700</xmax>")
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "invalid.xml"
            xml_path.write_text(invalid, encoding="utf-8")

            with self.assertRaises(ValueError):
                voc_xml_to_label_studio_task(xml_path)


if __name__ == "__main__":
    unittest.main()
