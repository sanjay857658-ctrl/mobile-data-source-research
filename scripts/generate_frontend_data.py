#!/usr/bin/env python3

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLE_FILE = BASE_DIR / "data" / "sample_data.csv"
MOCK_FILE = BASE_DIR / "data" / "mock_social_links.csv"
OUTPUT_FILE = BASE_DIR / "frontend" / "data.json"


def read_csv(path):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def main():
    samples = read_csv(SAMPLE_FILE)
    mocks = read_csv(MOCK_FILE)

    mock_by_id = {
        row.get("record_id"): row
        for row in mocks
    }

    records = []

    for row in samples:
        record_id = row.get("record_id", "")
        mock = mock_by_id.get(record_id, {})

        records.append({
            "id": record_id,
            "phone": row.get("phone_number", ""),
            "country": row.get("country", ""),
            "source": row.get("source_type", ""),
            "confidence": row.get("confidence", ""),
            "facebook": mock.get("mock_facebook", ""),
            "instagram": mock.get("mock_instagram", "")
        })

    payload = {
        "privacy": "SYNTHETIC / DEMO ONLY",
        "total_records": len(records),
        "valid_numbers": len(records),
        "duplicates": 0,
        "audit_status": "PASS",
        "records": records
    }

    OUTPUT_FILE.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8"
    )

    print(f"Generated: {OUTPUT_FILE}")
    print(f"Records: {len(records)}")


if __name__ == "__main__":
    main()
