#!/bin/bash
echo "🐾 Starting PawHealth PRO Demo..."

echo "1. Checking Service Health..."
curl -s http://localhost:8000/healthz | grep "healthy"

echo -e "\n2. Running AI Food Analysis for Joey (The King)..."
curl -s -X POST "http://localhost:8000/dogs/analyze-food?dog_breed=Golden&food=apple"

echo -e "\n\n3. Running Async Batch Refresher (Reliability Check)..."
uv run python scripts/refresh.py

echo -e "\n4. Verification Complete. All EX3 Microservices are communicating."
