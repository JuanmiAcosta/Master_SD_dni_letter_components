#!/usr/bin/env bash
# Cliente curl para el microservicio DNI.
# Uso: ./client/client.sh [URL_BASE]   (por defecto http://127.0.0.1:8000)
set -euo pipefail

API_URL="${1:-${API_URL:-http://127.0.0.1:8000}}"

echo "== POST /dni/12345678 (calcular letra)"
curl -s -X POST "$API_URL/dni/12345678"
echo

echo "== GET /dni/validar?dni=12345678Z (DNI válido)"
curl -s "$API_URL/dni/validar?dni=12345678Z"
echo

echo "== GET /dni/validar?dni=12345678A (letra incorrecta)"
curl -s "$API_URL/dni/validar?dni=12345678A"
echo

echo "== POST /dni/123456789 (fuera de rango -> 422)"
curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "$API_URL/dni/123456789"
