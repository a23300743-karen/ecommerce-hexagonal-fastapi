#!/usr/bin/env bash
set -euo pipefail

echo "=== Contenedores ==="
docker compose ps

echo
echo "=== Blue directo ==="
curl --silent http://127.0.0.1:8001/deployment || true

echo
echo "=== Green directo ==="
curl --silent http://127.0.0.1:8002/deployment || true

echo
echo "=== Trafico por Nginx ==="
curl --silent http://127.0.0.1:8080/deployment || true
echo
