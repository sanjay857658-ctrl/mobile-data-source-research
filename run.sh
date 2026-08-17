#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "================================================"
echo "MOBILE DATA SOURCE RESEARCH"
echo "SAFE EDUCATIONAL WORKFLOW"
echo "================================================"

echo
echo "[1/5] Generating synthetic social-link dataset..."
python scripts/generate_mock_links.py

echo
echo "[2/5] Generating frontend data..."
python scripts/generate_frontend_data.py

echo
echo "[3/5] Running dataset analysis..."
python scripts/collector.py

echo
echo "[4/5] Running automated safety audit..."
python scripts/safety_audit.py

echo
echo "[5/5] Checking Git status..."
git status --short

echo
echo "================================================"
echo "WORKFLOW COMPLETE"
echo "================================================"
echo "No automatic GitHub push was performed."
