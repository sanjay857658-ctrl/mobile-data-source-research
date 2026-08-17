#!/usr/bin/env python3

import csv
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_FILE = BASE_DIR / "data" / "sample_data.csv"
MOCK_FILE = BASE_DIR / "data" / "mock_social_links.csv"


def read_csv(path):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_data():
    samples = read_csv(DATA_FILE)
    mocks = read_csv(MOCK_FILE)

    mock_by_id = {
        row.get("record_id"): row
        for row in mocks
    }

    records = []

    for row in samples:
        rid = row.get("record_id", "")
        mock = mock_by_id.get(rid, {})

        records.append({
            "id": rid,
            "phone": row.get("phone_number", ""),
            "country": row.get("country", ""),
            "number_type": row.get("number_type", ""),
            "source_type": row.get("source_type", ""),
            "source_name": row.get("source_name", ""),
            "data_found": row.get("data_found", ""),
            "consent_status": row.get("consent_status", ""),
            "confidence": row.get("confidence", ""),
            "notes": row.get("notes", ""),
            "mock_facebook": mock.get("mock_facebook", ""),
            "mock_instagram": mock.get("mock_instagram", ""),
        })

    return {
        "privacy_status": "SAFE / LOCAL / SYNTHETIC",
        "real_lookup": False,
        "total_records": len(records),
        "records": records,
    }


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/api/data":
            payload = json.dumps(
                build_data(),
                ensure_ascii=False
            ).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        super().do_GET()


if __name__ == "__main__":
    print("=" * 60)
    print("MOBILE DATA SOURCE RESEARCH")
    print("LOCAL EDUCATIONAL API")
    print("=" * 60)
    print("Real-person lookup : DISABLED")
    print("Server             : http://127.0.0.1:8080")
    print("=" * 60)

    server = ThreadingHTTPServer(
        ("127.0.0.1", 8080),
        lambda *args, **kwargs:
            Handler(*args, directory=str(FRONTEND_DIR), **kwargs)
    )

    server.serve_forever()
