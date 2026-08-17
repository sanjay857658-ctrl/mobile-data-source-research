#!/usr/bin/env python3

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "mock_social_links.csv"


def generate():
    with INPUT_FILE.open("r", encoding="utf-8", newline="") as infile:
        rows = list(csv.DictReader(infile))

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as outfile:
        fieldnames = [
            "record_id",
            "phone_number",
            "mock_facebook",
            "mock_instagram",
            "source_type",
            "confidence",
        ]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            record_id = row["record_id"]

            writer.writerow({
                "record_id": record_id,
                "phone_number": row["phone_number"],
                "mock_facebook":
                    f"https://example.com/facebook/test-user-{int(record_id):03d}",
                "mock_instagram":
                    f"https://example.com/instagram/test-user-{int(record_id):03d}",
                "source_type": "synthetic",
                "confidence": "demo_only",
            })

    print(f"Generated: {OUTPUT_FILE}")
    print(f"Records: {len(rows)}")


if __name__ == "__main__":
    generate()
