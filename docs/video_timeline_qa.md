# Video action timeline metadata QA

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_video_action_timeline.py' -v
python -m unittest discover -s tests -p 'test_video_action_taxonomy.py' -v
python tools/validate_video_action_timeline.py samples/video_action_annotation_practice.csv
python tools/validate_video_action_timeline.py samples/video_action_annotation_practice.csv --taxonomy samples/video_action_taxonomy.json
```

The validator rejects duplicate column names and checks required columns, essential nonempty fields, valid timestamps,
positive segment duration, and overlapping intervals **within the same clip**.
It also rejects short CSV records with omitted trailing cells and rows containing extra fields.
Explicit empty cells remain valid for optional annotation fields.
Adjacent segments and overlapping timestamps across different clips are allowed.
CSV rows may be unsorted. Errors include source line numbers. Malformed quoting is rejected
instead of being silently accepted; parse errors report the physical source line, including
multiline quoted records.

An optional JSON taxonomy file can constrain project-specific categorical values for `actor`, `action`,
`interaction`, `instruction_alignment`, and `confidence`. Only fields listed in the file are checked.
Values are compared case-sensitively after surrounding whitespace is trimmed. Empty cells are left
unconstrained so optional metadata can remain blank. `object` and `end_state` are intentionally not
included in the supported taxonomy fields because they may contain free-text identifiers or outcomes.

The bundled `samples/video_action_taxonomy.json` is a narrow allowlist for the synthetic practice CSV only;
it is not a universal robotics or human-activity taxonomy. Replace it with the vocabulary approved for the
specific annotation project before using this check on another dataset.

**Limitations:** This is metadata-only QA. It cannot establish whether an action
label, actor, temporal boundary, or instruction alignment is correct from the video.
It does not enforce exhaustive temporal coverage or a fixed universal action taxonomy:
those require a project-specific annotation rubric. The example CSV is synthetic
practice material, not commercial annotation work.
