"""Validate timestamp, schema, and optional taxonomy integrity of video-action CSV annotations.

This checks metadata consistency, not whether labels match video content.
"""
import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REQUIRED = ("clip_id", "start_time", "end_time", "actor", "action", "object",
            "interaction", "end_state", "instruction_alignment", "confidence", "reviewer_note")
TAXONOMY_FIELDS = frozenset((
    "actor", "action", "interaction", "instruction_alignment", "confidence"
))
TIME = re.compile(r"^(?:(\d+):)?(\d{2}):(\d{2})\.(\d{3})$")


def seconds(value):
    match = TIME.fullmatch(value.strip())
    if not match:
        raise ValueError("expected MM:SS.mmm or HH:MM:SS.mmm")
    hours, minutes, secs, millis = match.groups()
    if int(secs) >= 60 or (hours is not None and int(minutes) >= 60):
        raise ValueError("seconds/minutes out of range")
    return (int(hours or 0) * 3600 + int(minutes) * 60
            + int(secs) + int(millis) / 1000)


def load_taxonomy(path):
    """Load a project-specific JSON allowlist for supported categorical fields."""
    try:
        with open(path, encoding="utf-8") as stream:
            raw = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read taxonomy: {exc}") from exc

    if not isinstance(raw, dict) or not raw:
        raise ValueError("taxonomy must be a non-empty JSON object")

    taxonomy = {}
    for field, values in raw.items():
        if field not in TAXONOMY_FIELDS:
            supported = ", ".join(sorted(TAXONOMY_FIELDS))
            raise ValueError(f"unsupported taxonomy field {field!r}; supported fields: {supported}")
        if not isinstance(values, list) or not values:
            raise ValueError(f"taxonomy field {field!r} must contain a non-empty list")
        normalized = []
        for value in values:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"taxonomy values for {field!r} must be non-empty strings")
            label = value.strip()
            if label in normalized:
                raise ValueError(f"duplicate taxonomy value {label!r} for {field!r}")
            normalized.append(label)
        taxonomy[field] = frozenset(normalized)
    return taxonomy


def validate(path, taxonomy=None):
    errors = []
    timelines = defaultdict(list)
    taxonomy = taxonomy or {}
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream, strict=True)
        try:
            headers = reader.fieldnames or []
        except csv.Error as exc:
            return [f"line {reader.reader.line_num}: malformed CSV: {exc}"]
        seen = set()
        duplicates = set()
        for name in headers:
            if name in seen:
                duplicates.add(name)
            seen.add(name)
        if duplicates:
            return ["duplicate columns: " + ", ".join(sorted(duplicates))]
        missing = [name for name in REQUIRED if name not in headers]
        if missing:
            return ["missing columns: " + ", ".join(missing)]
        try:
            for row in reader:
                # DictReader.line_num counts physical CSV lines, including lines
                # embedded in quoted fields; record enumeration does not.
                line = reader.line_num
                if None in row:
                    errors.append(f"line {line}: extra CSV fields")
                    continue
                # DictReader assigns None to trailing columns omitted from a
                # short row. Explicit empty cells remain empty strings and are allowed.
                missing_values = [name for name in headers if row[name] is None]
                if missing_values:
                    errors.append(
                        f"line {line}: missing CSV values: {', '.join(missing_values)}"
                    )
                    continue
                for name in ("clip_id", "start_time", "end_time", "actor", "action"):
                    if not (row[name] or "").strip():
                        errors.append(f"line {line}: empty {name}")
                for name, allowed in taxonomy.items():
                    value = (row.get(name) or "").strip()
                    if value and value not in allowed:
                        expected = ", ".join(sorted(allowed))
                        errors.append(
                            f"line {line}: unknown {name} value {value!r}; expected one of: {expected}"
                        )
                try:
                    start = seconds(row["start_time"] or "")
                    end = seconds(row["end_time"] or "")
                except ValueError as exc:
                    errors.append(f"line {line}: invalid timestamp: {exc}")
                    continue
                if end <= start:
                    errors.append(f"line {line}: end_time must exceed start_time")
                clip = (row["clip_id"] or "").strip()
                if clip:
                    timelines[clip].append((start, end, line))
        except csv.Error as exc:
            # The underlying csv.reader tracks physical lines consumed on parse errors.
            errors.append(f"line {reader.reader.line_num}: malformed CSV: {exc}")
    for clip, intervals in timelines.items():
        intervals.sort()
        # Track the interval with the furthest end: adjacent-only checks
        # miss overlaps when a long segment contains multiple shorter ones.
        latest_end = None
        latest_line = None
        for start, end, line in intervals:
            if latest_end is not None and start < latest_end:
                errors.append(f"clip {clip}: overlapping intervals on lines {latest_line} and {line}")
            if latest_end is None or end > latest_end:
                latest_end, latest_line = end, line
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--taxonomy", type=Path,
        help="optional project-specific JSON allowlist for categorical annotation fields",
    )
    args = parser.parse_args()
    try:
        taxonomy = load_taxonomy(args.taxonomy) if args.taxonomy else None
    except ValueError as exc:
        print(f"taxonomy error: {exc}")
        return 2
    errors = validate(args.csv_path, taxonomy=taxonomy)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Timeline metadata QA passed (visual label accuracy not assessed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
