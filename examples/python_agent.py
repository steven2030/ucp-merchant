"""
Example UCP Agent in Python

This agent demonstrates a complete shopping flow:
1. Discover merchant capabilities
2. Browse products
3. Make a purchase
4. Check order status
"""

import requests

BASE_URL = "https://puddingheroes.com"  # Or http://localhost:5000 for local


def main():
    print("=" * 60)
    print("UCP Agent Demo")
    print("=" * 60)

    # Step 1: Discovery
    print("\n[1] Discovering merchant...")
    discovery = requests.get(f"{BASE_URL}/.well-known/ucp.json").json()
    merchant = discovery["ucp"]["merchant"]
    print(f"    Merchant: {merchant['name']}")
    print(f"    Description: {merchant['description']}")
    print(f"    Sandbox mode: {discovery['ucp']['sandbox']}")

    # Step 2: List products
    print("\n[2] Fetching product catalog...")
    products = requests.get(f"{BASE_URL}/api/ucp/products").json()
    print(f"    Found {products['count']} products:")
    for p in products["products"]:
        print(f"    - {p['name']}: ${p['price']} ({p['type']})")

    # Step 3: Get free products
    print("\n[3] Finding free products...")
    free_products = requests.get(
        f"{BASE_URL}/api/ucp/products?max_price=0"
    ).json()
    print(f"    Found {free_products['count']} free items")

    # Step 4: Make a purchase
    print("\n[4] Purchasing 'Pudding Theory' PDF...")
    order = requests.post(
        f"{BASE_URL}/api/ucp/checkout",
        json={
            "line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}],
            "buyer": {"name": "Python Agent", "email": "agent@example.com"},
            "payment_token": "sandbox_test",
        },
    ).json()

    print(f"    Order ID: {order['order_id']}")
    print(f"    Status: {order['status']}")
    print(f"    Total: ${order['totals']['total']}")

    # Step 5: Get download link
    if order.get("fulfillment"):
        fulfillment = order["fulfillment"][0]
        print(f"\n[5] Fulfillment:")
        print(f"    Type: {fulfillment['type']}")
        print(f"    Status: {fulfillment['status']}")
        if "download_url" in fulfillment:
            print(f"    Download URL: {fulfillment['download_url']}")

    # Step 6: Check order status
    print(f"\n[6] Checking order status...")
    order_status = requests.get(
        f"{BASE_URL}/api/ucp/orders/{order['order_id']}"
    ).json()
    print(f"    Order {order_status['order_id']}: {order_status['status']}")

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
