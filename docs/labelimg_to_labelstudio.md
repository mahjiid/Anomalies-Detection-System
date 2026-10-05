# LabelImg → Label Studio migration utility

This utility converts LabelImg **Pascal VOC XML** bounding-box annotations into
Label Studio JSON tasks.

It was added as part of my annotation portfolio because I have used LabelImg for
image bounding-box annotation and wanted to document a reproducible migration
path into a modern annotation platform.

## What it converts

- LabelImg Pascal VOC XML
- image filename
- image width/height
- object class names
- bounding boxes

Absolute pixel coordinates are converted to Label Studio percentage coordinates.

## Usage

```bash
python tools/labelimg_voc_to_labelstudio.py path/to/xml \
  --out label_studio_tasks.json \
  --image-prefix "/data/local-files/?d=images"
```

The default Label Studio tag names are:

- control tag: `label`
- image tag/data key: `image`

Override them with `--from-name` and `--to-name` when your labeling config
uses different names.

## Validation

The converter rejects:

- missing image dimensions
- zero/negative image dimensions
- objects without bounding boxes
- non-numeric coordinates
- boxes outside the image
- boxes where xmin >= xmax or ymin >= ymax

This is intentional: annotation migration should fail loudly rather than silently
introduce incorrect ground truth.

## Example

A sample LabelImg XML file is available at
`samples/labelimg_example.xml`.

For a 640×480 image with a box from `(64, 96)` to `(320, 240)`, the Label
Studio rectangle becomes:

- x = 10%
- y = 20%
- width = 40%
- height = 30%

## Portfolio relevance

This demonstrates practical understanding of:

- LabelImg / Pascal VOC annotation format
- bounding-box QA
- annotation metadata
- coordinate-system conversion
- dataset migration
- Label Studio task structure
- human-in-the-loop data workflows
