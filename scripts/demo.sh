#!/bin/bash
echo "🐾 Starting PawHealth Pro Demo..."

echo "1. Checking Service Health..."
curl -s http://localhost:8000/healthz | python3 -m json.tool

echo -e "\n2. Creating a sample patient..."
curl -s -X POST http://localhost:8000/dogs \
  -H "Content-Type: application/json" \
  -d '{"name":"Joey","breed":"Golden Retriever","age":3,"ideal_weight_kg":30.0}' \
  | python3 -m json.tool

echo -e "\n3. Listing all patients..."
curl -s http://localhost:8000/dogs | python3 -m json.tool

echo -e "\n4. Running Async Batch Refresher (bounded concurrency + Redis idempotency)..."
uv run python scripts/refresh.py

echo -e "\n5. Demonstrating CSV export (Registry tab enhancement)..."
echo "   Fetching all patients and formatting as CSV:"
curl -s http://localhost:8000/dogs | python3 -c "
import sys, json, csv
dogs = json.load(sys.stdin)
fields = ['id','name','breed','age','current_weight_kg','ideal_weight_kg','is_favorite']
w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction='ignore')
w.writeheader()
w.writerows(dogs)
"

echo -e "\n6. Verification complete. Open http://localhost:8501 for the full dashboard (Registry → Export Registry as CSV)."
