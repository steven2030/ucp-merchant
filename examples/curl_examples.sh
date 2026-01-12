#!/bin/bash
# UCP API Examples using curl
# Usage: ./curl_examples.sh [base_url]

BASE_URL="${1:-https://puddingheroes.com}"

echo "========================================"
echo "UCP API Examples"
echo "Base URL: $BASE_URL"
echo "========================================"

echo ""
echo "=== Discovery ==="
echo "curl $BASE_URL/.well-known/ucp.json"
curl -s "$BASE_URL/.well-known/ucp.json" | head -20
echo "..."

echo ""
echo "=== List All Products ==="
echo "curl $BASE_URL/api/ucp/products"
curl -s "$BASE_URL/api/ucp/products" | head -30
echo "..."

echo ""
echo "=== Filter: Digital Products Under \$5 ==="
echo "curl '$BASE_URL/api/ucp/products?type=digital&max_price=5'"
curl -s "$BASE_URL/api/ucp/products?type=digital&max_price=5"

echo ""
echo "=== Get Single Product ==="
echo "curl $BASE_URL/api/ucp/products/pudding-theory-pdf"
curl -s "$BASE_URL/api/ucp/products/pudding-theory-pdf"

echo ""
echo "=== Check Availability (for bookings) ==="
echo "curl $BASE_URL/api/ucp/products/signal-house-1night/availability"
curl -s "$BASE_URL/api/ucp/products/signal-house-1night/availability"

echo ""
echo "=== Checkout (Purchase) ==="
echo 'curl -X POST "$BASE_URL/api/ucp/checkout" -H "Content-Type: application/json" -d {...}'
curl -s -X POST "$BASE_URL/api/ucp/checkout" \
  -H "Content-Type: application/json" \
  -d '{
    "line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}],
    "buyer": {"name": "Curl Agent", "email": "curl@example.com"},
    "payment_token": "sandbox_test"
  }'

echo ""
echo ""
echo "=== Quick Test Endpoint ==="
echo "curl $BASE_URL/api/ucp/test"
curl -s "$BASE_URL/api/ucp/test"

echo ""
echo ""
echo "=== API Docs ==="
echo "curl $BASE_URL/api/ucp/docs"
curl -s "$BASE_URL/api/ucp/docs"

echo ""
echo ""
echo "========================================"
echo "Done!"
echo "========================================"
