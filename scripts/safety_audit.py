#!/usr/bin/env python3

import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sample_data.csv"
MOCK_FILE = BASE_DIR / "data" / "mock_social_links.csv"

REQUIRED_COLUMNS = {
    "record_id",
    "phone_number",
    "country",
    "number_type",
    "source_type",
    "source_name",
    "data_found",
    "consent_status",
    "confidence",
    "notes",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{10,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"api[_-]?key\s*[:=]", re.I),
    re.compile(r"password\s*[:=]", re.I),
    re.compile(r"secret\s*[:=]", re.I),
]


def check_dataset():
    print("[1] Checking sample dataset...")

    if not DATA_FILE.exists():
        print("FAIL: sample_data.csv not found")
        return False

    with DATA_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        columns = set(reader.fieldnames or [])
        rows = list(reader)

    missing = REQUIRED_COLUMNS - columns

    if missing:
        print(f"FAIL: missing columns: {sorted(missing)}")
        return False

    if not rows:
        print("FAIL: dataset contains no records")
        return False

    numbers = [
        row.get("phone_number", "").strip()
        for row in rows
    ]

    if any(not number for number in numbers):
        print("FAIL: empty phone-number field detected")
        return False

    duplicates = len(numbers) - len(set(numbers))

    if duplicates:
        print(f"FAIL: duplicate numbers detected: {duplicates}")
        return False

    invalid_sources = [
        row for row in rows
        if row.get("source_type") != "synthetic"
    ]

    if invalid_sources:
        print("FAIL: non-synthetic source detected")
        return False

    print(f"PASS: {len(rows)} synthetic records")
    return True


def check_mock_file():
    print("\n[2] Checking mock social-link dataset...")

    if not MOCK_FILE.exists():
        print("FAIL: mock_social_links.csv not found")
        return False

    with MOCK_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("FAIL: mock dataset is empty")
        return False

    for row in rows:
        facebook = row.get("mock_facebook", "")
        instagram = row.get("mock_instagram", "")

        if "example.com" not in facebook:
            print("FAIL: unexpected Facebook URL")
            return False

        if "example.com" not in instagram:
            print("FAIL: unexpected Instagram URL")
            return False

    print(f"PASS: {len(rows)} synthetic mock links")
    return True


def scan_for_secrets():
    print("\n[3] Scanning project files for obvious secrets...")

    allowed = {
        ".py",
        ".md",
        ".csv",
        ".sh",
        ".txt",
    }

    found = []

    for path in BASE_DIR.rglob("*"):
        if not path.is_file():
            continue

        if ".git" in path.parts:
            continue

        if path.suffix not in allowed:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                found.append(str(path.relative_to(BASE_DIR)))
                break

    if found:
        print("FAIL: possible secret pattern found:")
        for item in found:
            print(f"  - {item}")
        return False

    print("PASS: no obvious secret patterns found")
    return True


def main():
    print("=" * 64)
    print("MOBILE DATA SOURCE RESEARCH")
    print("AUTOMATED SAFETY AUDIT")
    print("=" * 64)

    results = [
        check_dataset(),
        check_mock_file(),
        scan_for_secrets(),
    ]

    print("\n" + "=" * 64)

    if all(results):
        print("AUDIT RESULT: PASS")
        print("Project appears safe for the synthetic educational dataset.")
        print("=" * 64)
        return 0

    print("AUDIT RESULT: FAIL")
    print("Review the reported problems before committing/pushing.")
    print("=" * 64)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
