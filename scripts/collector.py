#!/usr/bin/env python3

"""
Mobile Data Source Research
Educational / Privacy-Safe Demo

This tool:
- Validates phone-number formatting
- Reads the local synthetic CSV dataset
- Checks duplicate records
- Produces basic dataset statistics

It does NOT:
- Search for people
- Query private databases
- Collect names, addresses or locations
- Perform identity lookup
- Scrape social-media accounts
"""

import csv
import re
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sample_data.csv"


PHONE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def normalize_phone(phone: str) -> str:
    """Remove common formatting characters."""
    return re.sub(r"[\s().-]", "", phone.strip())


def validate_phone(phone: str) -> bool:
    """Validate basic international phone-number format."""
    return bool(PHONE_PATTERN.fullmatch(normalize_phone(phone)))


def load_dataset():
    """Load the local CSV dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def analyze_dataset(rows):
    """Return safe dataset statistics."""
    total = len(rows)

    valid_numbers = 0
    invalid_numbers = 0
    numbers = []

    countries = Counter()
    source_types = Counter()
    confidence = Counter()

    for row in rows:
        phone = row.get("phone_number", "")
        normalized = normalize_phone(phone)

        if validate_phone(phone):
            valid_numbers += 1
        else:
            invalid_numbers += 1

        numbers.append(normalized)

        countries[row.get("country", "unknown")] += 1
        source_types[row.get("source_type", "unknown")] += 1
        confidence[row.get("confidence", "unknown")] += 1

    duplicates = total - len(set(numbers))

    return {
        "total_records": total,
        "valid_numbers": valid_numbers,
        "invalid_numbers": invalid_numbers,
        "duplicate_numbers": duplicates,
        "countries": countries,
        "source_types": source_types,
        "confidence": confidence,
    }


def print_report(stats):
    """Display a human-readable report."""
    print("=" * 64)
    print("MOBILE DATA SOURCE RESEARCH")
    print("SAFE EDUCATIONAL DATASET ANALYSIS")
    print("=" * 64)

    print(f"Total records       : {stats['total_records']}")
    print(f"Valid numbers      : {stats['valid_numbers']}")
    print(f"Invalid numbers    : {stats['invalid_numbers']}")
    print(f"Duplicate numbers  : {stats['duplicate_numbers']}")

    print("\nCountries")
    print("-" * 64)
    for country, count in stats["countries"].items():
        print(f"{country:20} : {count}")

    print("\nSource types")
    print("-" * 64)
    for source, count in stats["source_types"].items():
        print(f"{source:20} : {count}")

    print("\nConfidence")
    print("-" * 64)
    for level, count in stats["confidence"].items():
        print(f"{level:20} : {count}")

    print("\nPrivacy status     : SAFE / LOCAL / SYNTHETIC")
    print("=" * 64)


def main():
    try:
        rows = load_dataset()
        stats = analyze_dataset(rows)
        print_report(stats)

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)

    except csv.Error as error:
        print(f"CSV ERROR: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
