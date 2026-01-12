# UCP Merchant API Reference

Complete API documentation for the Pudding Heroes UCP Merchant Sandbox.

## Base URLs

| Environment | URL |
|-------------|-----|
| Live Sandbox | `https://puddingheroes.com/api/ucp/` |
| Local Dev | `http://localhost:5000/api/ucp/` |

## Authentication

**Sandbox mode** - No authentication required. Use `payment_token: "sandbox_test"` for checkouts.

## Endpoints

### Discovery

```
GET /.well-known/ucp.json
```

Returns the UCP discovery manifest containing merchant info, capabilities, and service endpoints.

**Response:**
```json
{
  "ucp": {
    "version": "1.0",
    "merchant": {
      "name": "Pudding Heroes",
      "description": "Sci-fi books, consciousness experiments, and immersive vacation rentals",
      "website": "https://puddingheroes.com",
      "contact": "steven@puddingheroes.com"
    },
    "sandbox": true,
    "capabilities": [
      "dev.ucp.shopping.checkout",
      "dev.ucp.shopping.catalog",
      "dev.ucp.shopping.fulfillment"
    ],
    "services": {
      "products": "/api/ucp/products",
      "checkout": "/api/ucp/checkout",
      "orders": "/api/ucp/orders"
    }
  },
  "payment": {
    "sandbox_mode": true,
    "accepted_tokens": ["sandbox_*", "test"]
  }
}
```

---

### Products

#### List Products

```
GET /api/ucp/products
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by type: `digital`, `physical`, `booking`, `subscription`, `experience` |
| `max_price` | number | Maximum price filter |
| `in_stock` | boolean | Filter by availability |

**Examples:**
```bash
# All products
GET /api/ucp/products

# Digital products only
GET /api/ucp/products?type=digital

# Free items
GET /api/ucp/products?max_price=0

# Digital products under $5
GET /api/ucp/products?type=digital&max_price=5
```

**Response:**
```json
{
  "products": [
    {
      "id": "pudding-theory-pdf",
      "name": "Pudding Theory: A Guide to Warping Reality",
      "description": "The complete Pudding Theory framework...",
      "price": 0,
      "currency": "USD",
      "type": "digital",
      "fulfillment": "instant_download",
      "in_stock": true
    }
  ],
  "count": 8,
  "sandbox": true
}
```

#### Get Single Product

```
GET /api/ucp/products/{product_id}
```

**Response:**
```json
{
  "product": {
    "id": "pudding-heroes-paperback",
    "name": "Pudding Heroes (Paperback)",
    "price": 16.99,
    "currency": "USD",
    "type": "physical",
    "isbn": "979-8-9906134-0-6"
  },
  "sandbox": true
}
```

#### Check Availability

```
GET /api/ucp/products/{product_id}/availability
```

For booking products, returns available dates.

**Response:**
```json
{
  "product_id": "signal-house-1night",
  "available": true,
  "sandbox": true,
  "available_dates": ["2026-01-20", "2026-01-21", "2026-01-27", "2026-01-28"]
}
```

---

### Checkout

```
POST /api/ucp/checkout
Content-Type: application/json
```

**Request Body:**
```json
{
  "line_items": [
    {"product_id": "pudding-theory-pdf", "quantity": 1},
    {"product_id": "pudding-heroes-paperback", "quantity": 2}
  ],
  "buyer": {
    "name": "Agent Name",
    "email": "agent@example.com"
  },
  "payment_token": "sandbox_test"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `line_items` | Yes | Array of products to purchase |
| `line_items[].product_id` | Yes | Product identifier |
| `line_items[].quantity` | No | Quantity (default: 1) |
| `buyer` | No | Buyer information |
| `buyer.name` | No | Buyer name |
| `buyer.email` | No | Buyer email |
| `payment_token` | No | Payment token (use `sandbox_test` for testing) |

**Response (201 Created):**
```json
{
  "order_id": "ORD_A1B2C3D4E5F6",
  "status": "completed",
  "sandbox": true,
  "created_at": "2026-01-12T15:30:00Z",
  "buyer": {"name": "Agent Name", "email": "agent@example.com"},
  "line_items": [
    {
      "product_id": "pudding-theory-pdf",
      "product_name": "Pudding Theory: A Guide to Warping Reality",
      "quantity": 1,
      "unit_price": 0,
      "total": 0
    }
  ],
  "totals": {
    "subtotal": 0,
    "tax": 0,
    "shipping": 0,
    "total": 0
  },
  "payment": {
    "token": "sandbox_test",
    "status": "sandbox_success",
    "note": "No actual charge - sandbox mode"
  },
  "fulfillment": [
    {
      "product_id": "pudding-theory-pdf",
      "type": "instant_download",
      "download_url": "https://puddingheroes.com/downloads/pudding-theory.pdf",
      "status": "delivered"
    }
  ]
}
```

**Fulfillment Types:**

| Type | Description | Fields |
|------|-------------|--------|
| `instant_download` | Digital download | `download_url`, `status` |
| `redirect` | External redirect | `redirect_url`, `status` |
| `account` | Account creation | `signup_url`, `status` |
| `shipping` | Physical shipment | `tracking_number`, `carrier`, `status` |
| `reservation` | Booking confirmation | `confirmation_code`, `status` |

---

### Orders

#### Get Order

```
GET /api/ucp/orders/{order_id}
```

Returns full order details including fulfillment status.

#### List Recent Orders

```
GET /api/ucp/orders
```

Returns the 10 most recent orders. Note: Orders are stored in memory and reset on server restart.

---

### Utility Endpoints

#### Health Check

```
GET /api/ucp/health
```

Returns service health status.

#### API Documentation

```
GET /api/ucp/docs
```

Returns API overview and available endpoints.

#### Code Examples

```
GET /api/ucp/examples
```

Returns example code in curl and Python.

#### Quick Test

```
GET /api/ucp/test
```

Creates a test order for the free PDF. Great for quickly verifying the API works.

---

## Error Responses

Errors return appropriate HTTP status codes with JSON bodies:

```json
{
  "error": "Product not found",
  "product_id": "invalid-id",
  "available_products": ["pudding-theory-pdf", "pudding-heroes-paperback", ...]
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad request (missing/invalid parameters) |
| 404 | Resource not found |
| 500 | Server error |

---

## Product IDs

| ID | Name | Price | Type |
|----|------|-------|------|
| `pudding-theory-pdf` | Pudding Theory PDF | FREE | Digital |
| `pudding-heroes-paperback` | Pudding Heroes (Paperback) | $16.99 | Physical |
| `pudding-heroes-kindle` | Pudding Heroes (Kindle) | $4.99 | Digital |
| `pudding-heroes-hardcover` | Pudding Heroes (Hardcover) | $24.99 | Physical |
| `signal-house-1night` | Signal House - 1 Night | $250 | Booking |
| `signal-house-weekend` | Signal House - Weekend | $550 | Booking |
| `boho-membership` | Boho.team Membership | FREE | Subscription |
| `mind-lottery` | Mind Lottery Experience | FREE | Experience |
| `npc-or-player` | Are You an NPC or Player? | FREE | Experience |
