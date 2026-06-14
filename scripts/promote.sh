#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"

if [[ "$TARGET" != "blue" && "$TARGET" != "green" ]]; then
  echo "Uso: ./scripts/promote.sh blue|green"
  exit 1
fi

SERVICE="app_${TARGET}"
PORT="8001"
if [[ "$TARGET" == "green" ]]; then
  PORT="8002"
fi

CURRENT="$(tr -d '\r\n' < nginx/active-environment 2>/dev/null || echo blue)"
echo "Ambiente actual: $CURRENT"
echo "Candidato: $TARGET"

docker compose up -d --build "$SERVICE"

echo "Esperando health check de $TARGET..."
for attempt in {1..30}; do
  if curl --fail --silent "http://127.0.0.1:${PORT}/health" > /tmp/ecommerce-health.json; then
    cat /tmp/ecommerce-health.json
    echo
    break
  fi

  if [[ "$attempt" == "30" ]]; then
    echo "La version $TARGET no esta saludable. El trafico permanece en $CURRENT."
    exit 1
  fi

  sleep 2
done

cp "nginx/${TARGET}-upstream.inc" nginx/active-upstream.inc

docker compose exec -T nginx nginx -t
docker compose exec -T nginx nginx -s reload
printf '%s\n' "$TARGET" > nginx/active-environment

echo "Promocion completada: el trafico ahora apunta a $TARGET."
curl --fail --silent http://127.0.0.1:8080/deployment
echo
