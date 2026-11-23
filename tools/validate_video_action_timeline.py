"""Validate timestamp and schema integrity of practice video-action CSV annotations.

This checks metadata consistency, not whether labels match video content.
"""
import argparse
import csv
import math
import re
from collections import defaultdict
from pathlib import Path

REQUIRED = ("clip_id", "start_time", "end_time", "actor", "action", "object",
            "interaction", "end_state", "instruction_alignment", "confidence", "reviewer_note")
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


def validate(path):
    errors = []
    timelines = defaultdict(list)
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
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
        for row in reader:
            # DictReader.line_num counts physical CSV lines, including lines
            # embedded in quoted fields; record enumeration does not.
            line = reader.line_num
            if None in row:
                errors.append(f"line {line}: extra CSV fields")
                continue
            for name in ("clip_id", "start_time", "end_time", "actor", "action"):
                if not (row[name] or "").strip():
                    errors.append(f"line {line}: empty {name}")
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
    args = parser.parse_args()
    errors = validate(args.csv_path)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Timeline metadata QA passed (visual label accuracy not assessed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
