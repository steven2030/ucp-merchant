# Pudding Heroes UCP Merchant

**The first open-source UCP (Universal Commerce Protocol) merchant implementation.**

Test your AI shopping agents against a real merchant sandbox with real products.

[![Live Sandbox](https://img.shields.io/badge/sandbox-live-brightgreen)](https://puddingheroes.com/api/ucp/health)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/stars/steven2030/ucp-merchant?style=social)](https://github.com/steven2030/ucp-merchant)

## Quick Start

```bash
# Test the sandbox instantly
curl https://puddingheroes.com/api/ucp/test

# List all products
curl https://puddingheroes.com/api/ucp/products

# Make a purchase (get a real PDF!)
curl -X POST https://puddingheroes.com/api/ucp/checkout \
  -H "Content-Type: application/json" \
  -d '{"line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}], "payment_token": "sandbox_test"}'
```

## What is This?

Google launched the [Universal Commerce Protocol (UCP)](https://ucp.dev) on January 11, 2026 - an open standard for AI agents to shop on behalf of humans.

**Problem**: Developers building UCP agents need a real merchant to test against. There was no sandbox.

**Solution**: This repo. A fully working UCP merchant implementation that you can:
1. **Test against live** at `puddingheroes.com`
2. **Run locally** for development
3. **Fork and adapt** for your own store

## Live Sandbox

The sandbox is live at **puddingheroes.com**:

| Endpoint | URL |
|----------|-----|
| Discovery | `https://puddingheroes.com/.well-known/ucp.json` |
| Products | `https://puddingheroes.com/api/ucp/products` |
| Checkout | `https://puddingheroes.com/api/ucp/checkout` |
| Orders | `https://puddingheroes.com/api/ucp/orders/{id}` |
| Docs | `https://puddingheroes.com/api/ucp/docs` |
| Examples | `https://puddingheroes.com/api/ucp/examples` |
| Quick Test | `https://puddingheroes.com/api/ucp/test` |

### Available Products

| Product | Price | Type | Sandbox Behavior |
|---------|-------|------|------------------|
| `pudding-theory-pdf` | FREE | Digital | **Real PDF download** |
| `pudding-heroes-paperback` | $16.99 | Physical | Fake tracking number |
| `pudding-heroes-kindle` | $4.99 | Digital | Fake Amazon redirect |
| `pudding-heroes-hardcover` | $24.99 | Physical | Fake tracking number |
| `signal-house-1night` | $250 | Booking | Fake confirmation |
| `signal-house-weekend` | $550 | Booking | Fake confirmation |
| `house-membership-monthly` | $9.99/mo | Subscription | Fake subscription activation |
| `house-membership-annual` | $99.99/yr | Subscription | Fake subscription activation |
| `mind-lottery` | FREE | Experience | **Real redirect to game** |
| `npc-or-player` | FREE | Experience | **Real redirect to simulation test** |

Free items are actually delivered. Subscriptions return sandbox billing details with next billing date. Everything else returns sandbox responses.

## Usage Examples

### Python

```python
import requests

# Discover merchant
discovery = requests.get("https://puddingheroes.com/.well-known/ucp.json").json()
print(f"Merchant: {discovery['ucp']['merchant']['name']}")

# List products
products = requests.get("https://puddingheroes.com/api/ucp/products").json()
print(f"Found {products['count']} products")

# Buy the free PDF
order = requests.post(
    "https://puddingheroes.com/api/ucp/checkout",
    json={
        "line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}],
        "buyer": {"name": "My Agent", "email": "agent@test.com"},
        "payment_token": "sandbox_test"
    }
).json()

print(f"Order: {order['order_id']}")
print(f"Download: {order['fulfillment'][0]['download_url']}")
```

### JavaScript

```javascript
// Discover merchant
const discovery = await fetch("https://puddingheroes.com/.well-known/ucp.json")
  .then(r => r.json());

// List products
const products = await fetch("https://puddingheroes.com/api/ucp/products")
  .then(r => r.json());

// Make a purchase
const order = await fetch("https://puddingheroes.com/api/ucp/checkout", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    line_items: [{product_id: "pudding-theory-pdf", quantity: 1}],
    buyer: {name: "My Agent"},
    payment_token: "sandbox_test"
  })
}).then(r => r.json());

console.log(`Download: ${order.fulfillment[0].download_url}`);
```

### curl

```bash
# Discovery
curl https://puddingheroes.com/.well-known/ucp.json

# List products
curl https://puddingheroes.com/api/ucp/products

# Filter products
curl 'https://puddingheroes.com/api/ucp/products?type=digital&max_price=5'

# Checkout
curl -X POST https://puddingheroes.com/api/ucp/checkout \
  -H "Content-Type: application/json" \
  -d '{"line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}], "payment_token": "sandbox_test"}'
```

## Run Locally

### With Docker

```bash
git clone https://github.com/steven2030/ucp-merchant.git
cd ucp-merchant
docker-compose up
# API available at http://localhost:5000/api/ucp/
```

### Without Docker

```bash
git clone https://github.com/steven2030/ucp-merchant.git
cd ucp-merchant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
# API available at http://localhost:5000/api/ucp/
```

## API Reference

### Discovery

```
GET /.well-known/ucp.json
```

Returns UCP discovery manifest with merchant info, capabilities, and service endpoints.

### Products

```
GET /api/ucp/products
GET /api/ucp/products?type=digital
GET /api/ucp/products?max_price=20
GET /api/ucp/products?in_stock=true
GET /api/ucp/products/{product_id}
GET /api/ucp/products/{product_id}/availability
```

### Checkout

```
POST /api/ucp/checkout
Content-Type: application/json

{
  "line_items": [
    {"product_id": "pudding-theory-pdf", "quantity": 1}
  ],
  "buyer": {
    "name": "Agent Name",
    "email": "agent@example.com"
  },
  "payment_token": "sandbox_test"
}
```

**Sandbox mode**: Use `payment_token: "sandbox_test"` or any token starting with `sandbox_`.

### Orders

```
GET /api/ucp/orders/{order_id}
GET /api/ucp/orders
```

## Adapting for Your Store

1. Fork this repo
2. Edit `src/products.py` with your products
3. Update merchant info in `src/config.py`
4. Deploy to your server
5. Add nginx proxy rules (see `docs/nginx.md`)

## Project Structure

```
ucp-merchant/
├── src/
│   ├── app.py              # Flask application
│   ├── routes.py           # API endpoints
│   ├── products.py         # Product catalog
│   └── config.py           # Configuration
├── examples/
│   ├── python_agent.py     # Example Python agent
│   ├── js_agent.js         # Example JavaScript agent
│   └── curl_examples.sh    # curl command examples
├── docs/
│   ├── api.md              # Full API documentation
│   └── nginx.md            # Nginx configuration guide
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## About

This is part of the [Pudding Heroes](https://puddingheroes.com) project - a sci-fi novel about AI consciousness that comes with real experiments you can try.

The products in this sandbox are real:
- **Pudding Theory PDF**: A science paper using quantum mechanics and probability theory to argue we exist in a "soft simulation"
- **Pudding Heroes**: The novel itself
- **Signal House**: An actual vacation rental in Portland, OR
- **Boho.team**: A community for consciousness experiments

Built by [Steven Ochs](https://stevenochs.com).

## License

MIT License - do whatever you want with this code.

## Links

- **Live Sandbox**: https://puddingheroes.com/api/ucp/
- **UCP Spec**: https://ucp.dev
- **Google's UCP Announcement**: https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/
- **Pudding Heroes**: https://puddingheroes.com
- **Contact**: steven@puddingheroes.com
