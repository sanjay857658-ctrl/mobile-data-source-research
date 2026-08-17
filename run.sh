#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "================================================"
echo "MOBILE DATA SOURCE RESEARCH"
echo "SAFE EDUCATIONAL WORKFLOW"
echo "================================================"

echo
echo "[1/3] Generating synthetic social-link dataset..."
python scripts/generate_mock_links.py

echo
echo "[2/3] Running dataset analysis..."
python scripts/collector.py

echo
echo "[3/3] Checking Git status..."
git status --short

echo
echo "================================================"
echo "WORKFLOW COMPLETE"
echo "================================================"
echo "No automatic GitHub push was performed."
