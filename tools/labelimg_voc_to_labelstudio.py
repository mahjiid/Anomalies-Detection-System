#!/usr/bin/env python3
"""Convert LabelImg Pascal VOC XML annotations into Label Studio JSON tasks.

This utility preserves bounding-box labels and image dimensions while converting
absolute VOC pixel coordinates into Label Studio's percentage-based rectangle
coordinates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def _required_text(parent: ET.Element, tag: str) -> str:
    node = parent.find(tag)
    if node is None or node.text is None or not node.text.strip():
        raise ValueError(f"Missing required <{tag}> element")
    return node.text.strip()


def _parse_float(parent: ET.Element, tag: str) -> float:
    try:
        return float(_required_text(parent, tag))
    except ValueError as exc:
        raise ValueError(f"Invalid numeric value in <{tag}>") from exc


def voc_xml_to_label_studio_task(
    xml_path: Path,
    *,
    image_prefix: str = "",
    from_name: str = "label",
    to_name: str = "image",
) -> dict:
    root = ET.parse(xml_path).getroot()

    filename = _required_text(root, "filename")
    size = root.find("size")
    if size is None:
        raise ValueError("Missing required <size> element")

    width = _parse_float(size, "width")
    height = _parse_float(size, "height")
    if width <= 0 or height <= 0:
        raise ValueError("Image width and height must be positive")

    results = []
    for index, obj in enumerate(root.findall("object")):
        label = _required_text(obj, "name")
        box = obj.find("bndbox")
        if box is None:
            raise ValueError(f"Object #{index + 1} is missing <bndbox>")

        xmin = _parse_float(box, "xmin")
        ymin = _parse_float(box, "ymin")
        xmax = _parse_float(box, "xmax")
        ymax = _parse_float(box, "ymax")

        if not (0 <= xmin < xmax <= width and 0 <= ymin < ymax <= height):
            raise ValueError(
                f"Object #{index + 1} has an invalid bounding box "
                f"({xmin}, {ymin}, {xmax}, {ymax}) for image {width}x{height}"
            )

        results.append(
            {
                "from_name": from_name,
                "to_name": to_name,
                "type": "rectanglelabels",
                "original_width": int(width),
                "original_height": int(height),
                "image_rotation": 0,
                "value": {
                    "x": xmin / width * 100.0,
                    "y": ymin / height * 100.0,
                    "width": (xmax - xmin) / width * 100.0,
                    "height": (ymax - ymin) / height * 100.0,
                    "rotation": 0,
                    "rectanglelabels": [label],
                },
            }
        )

    image_ref = f"{image_prefix.rstrip('/')}/{filename}" if image_prefix else filename

    return {
        "data": {to_name: image_ref},
        "annotations": [{"result": results}],
        "meta": {
            "source": "LabelImg Pascal VOC",
            "source_xml": xml_path.name,
        },
    }


def convert_directory(
    xml_dir: Path,
    *,
    image_prefix: str = "",
    from_name: str = "label",
    to_name: str = "image",
) -> list[dict]:
    xml_files = sorted(xml_dir.glob("*.xml"))
    if not xml_files:
        raise ValueError(f"No XML files found in {xml_dir}")

    return [
        voc_xml_to_label_studio_task(
            path,
            image_prefix=image_prefix,
            from_name=from_name,
            to_name=to_name,
        )
        for path in xml_files
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert LabelImg Pascal VOC XML files to Label Studio JSON."
    )
    parser.add_argument("xml_dir", type=Path, help="Directory containing LabelImg XML files")
    parser.add_argument("-o", "--out", type=Path, required=True, help="Output JSON file")
    parser.add_argument(
        "--image-prefix",
        default="",
        help="Prefix for image paths/URLs, e.g. /data/local-files/?d=images",
    )
    parser.add_argument("--from-name", default="label", help="Label Studio control tag name")
    parser.add_argument("--to-name", default="image", help="Label Studio image tag/data key")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tasks = convert_directory(
        args.xml_dir,
        image_prefix=args.image_prefix,
        from_name=args.from_name,
        to_name=args.to_name,
    )
    args.out.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    print(f"Wrote {len(tasks)} task(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
