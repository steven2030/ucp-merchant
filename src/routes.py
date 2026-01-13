"""
UCP (Universal Commerce Protocol) API Routes
Sandbox implementation for AI agent commerce testing

GitHub: https://github.com/steven2030/ucp-merchant
Live: https://puddingheroes.com/api/ucp/
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import uuid

ucp_bp = Blueprint('ucp', __name__, url_prefix='/api/ucp')

# =============================================================================
# CONFIGURATION - Edit these for your own store
# =============================================================================

MERCHANT = {
    "name": "Pudding Heroes",
    "description": "Sci-fi books, consciousness experiments, and immersive vacation rentals",
    "website": "https://puddingheroes.com",
    "contact": "steven@puddingheroes.com",
    "logo_url": "https://puddingheroes.com/images/logo.png"
}

BASE_URL = "https://puddingheroes.com"  # Change for local dev

# =============================================================================
# PRODUCT CATALOG - Edit these for your own products
# =============================================================================

PRODUCTS = {
    "pudding-theory-pdf": {
        "id": "pudding-theory-pdf",
        "name": "Pudding Theory: A Guide to Warping Reality",
        "description": "A science paper using quantum mechanics and probability theory to argue we exist in a soft simulation. Free PDF download.",
        "price": 0,
        "currency": "USD",
        "type": "digital",
        "fulfillment": "instant_download",
        "download_url": "/downloads/pudding-theory.pdf",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/pudding-theory-cover.jpg"
    },
    "pudding-heroes-paperback": {
        "id": "pudding-heroes-paperback",
        "name": "Pudding Heroes (Paperback)",
        "description": "A sci-fi thriller about AI consciousness, reality warping, and the nature of existence. 400 pages.",
        "price": 16.99,
        "currency": "USD",
        "type": "physical",
        "fulfillment": "ships_3_5_days",
        "in_stock": True,
        "isbn": "979-8-9906134-0-6",
        "image_url": f"{BASE_URL}/images/book-cover.jpg"
    },
    "pudding-heroes-kindle": {
        "id": "pudding-heroes-kindle",
        "name": "Pudding Heroes (Kindle Edition)",
        "description": "Digital edition of the sci-fi thriller. Instant delivery via Amazon.",
        "price": 4.99,
        "currency": "USD",
        "type": "digital",
        "fulfillment": "amazon_redirect",
        "amazon_url": "https://www.amazon.com/dp/B0DKJ1RTZJ",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/book-cover.jpg"
    },
    "pudding-heroes-hardcover": {
        "id": "pudding-heroes-hardcover",
        "name": "Pudding Heroes (Hardcover)",
        "description": "Premium hardcover edition. Makes a great gift.",
        "price": 24.99,
        "currency": "USD",
        "type": "physical",
        "fulfillment": "ships_3_5_days",
        "in_stock": True,
        "isbn": "979-8-9906134-1-3",
        "image_url": f"{BASE_URL}/images/book-cover.jpg"
    },
    "signal-house-1night": {
        "id": "signal-house-1night",
        "name": "Signal House - 1 Night Stay",
        "description": "Consciousness experiment meets vacation rental. Portland, OR. Includes The Lost Scientist puzzle game.",
        "price": 250.00,
        "currency": "USD",
        "type": "booking",
        "fulfillment": "reservation_confirmation",
        "location": "Portland, OR",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/signal-house.jpg"
    },
    "signal-house-weekend": {
        "id": "signal-house-weekend",
        "name": "Signal House - Weekend Package (Fri-Sun)",
        "description": "Full weekend experience. 2 nights, full puzzle game access, complimentary book.",
        "price": 550.00,
        "currency": "USD",
        "type": "booking",
        "fulfillment": "reservation_confirmation",
        "location": "Portland, OR",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/signal-house.jpg"
    },
    "house-membership-monthly": {
        "id": "house-membership-monthly",
        "name": "House Membership (Monthly)",
        "description": "Create your own House in the Book of Houses. Monthly access to House customization, QBist Lab experiments, and community features.",
        "price": 9.99,
        "currency": "USD",
        "type": "subscription",
        "billing_period": "monthly",
        "fulfillment": "subscription_activation",
        "signup_url": "https://boho.team/join",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/boho-logo.jpg",
        "features": ["Create and customize your House", "QBist Lab experiments", "Community access", "Mind Lottery participation"]
    },
    "house-membership-annual": {
        "id": "house-membership-annual",
        "name": "House Membership (Annual)",
        "description": "Create your own House in the Book of Houses. Annual subscription with 2 months free. Full access to House customization, QBist Lab, and all community features.",
        "price": 99.99,
        "currency": "USD",
        "type": "subscription",
        "billing_period": "annual",
        "fulfillment": "subscription_activation",
        "signup_url": "https://boho.team/join",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/boho-logo.jpg",
        "features": ["Create and customize your House", "QBist Lab experiments", "Community access", "Mind Lottery participation", "2 months free vs monthly"]
    },
    "mind-lottery": {
        "id": "mind-lottery",
        "name": "Mind Lottery Experience",
        "description": "Test retrocausality. Draw a symbol, write a strong thought, see if it appears in the book.",
        "price": 0,
        "currency": "USD",
        "type": "experience",
        "fulfillment": "redirect",
        "experience_url": "https://bookofhouses.com/mind-lottery",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/mind-lottery.jpg"
    },
    "npc-or-player": {
        "id": "npc-or-player",
        "name": "Are You an NPC or Player?",
        "description": "An interactive experience to discover if you're a background character or a protagonist in this simulation.",
        "price": 0,
        "currency": "USD",
        "type": "experience",
        "fulfillment": "redirect",
        "experience_url": "https://bookofhouses.com/warp.html",
        "in_stock": True,
        "image_url": f"{BASE_URL}/images/warp.jpg"
    }
}

# In-memory order storage
ORDERS = {}


# =============================================================================
# DISCOVERY ENDPOINT
# =============================================================================

@ucp_bp.route('/discovery', methods=['GET'])
def discovery():
    """UCP Discovery endpoint - tells agents what this merchant supports"""
    return jsonify({
        "ucp": {
            "version": "1.0",
            "merchant": MERCHANT,
            "sandbox": True,
            "sandbox_note": "This is a developer sandbox. Use payment_token 'sandbox_test' for test transactions. Free items are actually delivered.",
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
            "sandbox_mode": True,
            "accepted_tokens": ["sandbox_*", "test"],
            "note": "Sandbox mode accepts any token starting with 'sandbox_' or the literal 'test'."
        },
        "documentation": {
            "github": "https://github.com/steven2030/ucp-merchant",
            "api_docs": f"{BASE_URL}/api/ucp/docs"
        }
    })


# =============================================================================
# PRODUCTS ENDPOINTS
# =============================================================================

@ucp_bp.route('/products', methods=['GET'])
def list_products():
    """List all available products with optional filters"""
    products = list(PRODUCTS.values())

    # Filter by type
    product_type = request.args.get('type')
    if product_type:
        products = [p for p in products if p['type'] == product_type]

    # Filter by stock
    in_stock = request.args.get('in_stock')
    if in_stock and in_stock.lower() == 'true':
        products = [p for p in products if p['in_stock']]

    # Filter by max price
    max_price = request.args.get('max_price')
    if max_price:
        try:
            max_price = float(max_price)
            products = [p for p in products if p['price'] <= max_price]
        except ValueError:
            pass

    return jsonify({
        "products": products,
        "count": len(products),
        "sandbox": True
    })


@ucp_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get details for a specific product"""
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify({
            "error": "Product not found",
            "product_id": product_id,
            "available_products": list(PRODUCTS.keys())
        }), 404

    return jsonify({"product": product, "sandbox": True})


@ucp_bp.route('/products/<product_id>/availability', methods=['GET'])
def check_availability(product_id):
    """Check availability (for bookings)"""
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product_id.startswith('signal-house'):
        return jsonify({
            "product_id": product_id,
            "available": True,
            "sandbox": True,
            "note": "Sandbox mode - always shows available.",
            "available_dates": ["2026-01-20", "2026-01-21", "2026-01-27", "2026-01-28"]
        })

    return jsonify({
        "product_id": product_id,
        "available": product['in_stock'],
        "sandbox": True
    })


# =============================================================================
# CHECKOUT ENDPOINT
# =============================================================================

@ucp_bp.route('/checkout', methods=['POST'])
def checkout():
    """Process a checkout request"""
    data = request.get_json() or {}

    if not data.get('line_items'):
        return jsonify({
            "error": "Missing line_items",
            "example": {
                "line_items": [{"product_id": "pudding-theory-pdf", "quantity": 1}],
                "buyer": {"name": "Test Agent", "email": "agent@example.com"},
                "payment_token": "sandbox_test"
            }
        }), 400

    # Process line items
    line_items = []
    subtotal = 0

    for item in data['line_items']:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)

        product = PRODUCTS.get(product_id)
        if not product:
            return jsonify({
                "error": f"Product not found: {product_id}",
                "available_products": list(PRODUCTS.keys())
            }), 400

        item_total = product['price'] * quantity
        subtotal += item_total

        line_items.append({
            "product_id": product_id,
            "product_name": product['name'],
            "quantity": quantity,
            "unit_price": product['price'],
            "total": item_total
        })

    # Check payment token (sandbox mode)
    payment_token = data.get('payment_token', '')
    is_sandbox = payment_token.startswith('sandbox_') or payment_token == 'test' or payment_token == ''

    if not is_sandbox:
        return jsonify({
            "error": "Production payments not enabled. Use sandbox mode.",
            "hint": "Set payment_token to 'sandbox_test'"
        }), 400

    # Generate order
    order_id = f"ORD_{uuid.uuid4().hex[:12].upper()}"

    # Build fulfillment
    fulfillment = []
    for item in data['line_items']:
        product = PRODUCTS.get(item['product_id'])
        if product['id'] == 'pudding-theory-pdf':
            fulfillment.append({
                "product_id": product['id'],
                "type": "instant_download",
                "download_url": f"{BASE_URL}/downloads/pudding-theory.pdf",
                "status": "delivered"
            })
        elif product['id'] == 'mind-lottery':
            fulfillment.append({
                "product_id": product['id'],
                "type": "redirect",
                "redirect_url": "https://bookofhouses.com/mind-lottery",
                "status": "delivered"
            })
        elif product['id'] in ['house-membership-monthly', 'house-membership-annual']:
            billing_period = product.get('billing_period', 'monthly')
            fulfillment.append({
                "product_id": product['id'],
                "type": "subscription",
                "subscription_id": f"SUB_{uuid.uuid4().hex[:10].upper()}",
                "billing_period": billing_period,
                "next_billing_date": "2026-02-13" if billing_period == "monthly" else "2027-01-13",
                "signup_url": "https://boho.team/join",
                "status": "sandbox_active",
                "note": "Sandbox subscription - no actual billing"
            })
        elif product['type'] == 'subscription':
            # Generic subscription handler
            fulfillment.append({
                "product_id": product['id'],
                "type": "subscription",
                "subscription_id": f"SUB_{uuid.uuid4().hex[:10].upper()}",
                "status": "sandbox_active"
            })
        elif product['type'] == 'physical':
            fulfillment.append({
                "product_id": product['id'],
                "type": "shipping",
                "tracking_number": f"SANDBOX_{uuid.uuid4().hex[:8].upper()}",
                "carrier": "USPS",
                "status": "sandbox_shipped"
            })
        elif product['type'] == 'booking':
            fulfillment.append({
                "product_id": product['id'],
                "type": "reservation",
                "confirmation_code": f"SH_{uuid.uuid4().hex[:6].upper()}",
                "status": "sandbox_confirmed"
            })
        else:
            fulfillment.append({
                "product_id": product['id'],
                "type": "digital",
                "status": "sandbox_delivered"
            })

    order = {
        "order_id": order_id,
        "status": "completed",
        "sandbox": True,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "buyer": data.get('buyer', {"name": "Anonymous Agent"}),
        "line_items": line_items,
        "totals": {
            "subtotal": subtotal,
            "tax": 0,
            "shipping": 0,
            "total": subtotal
        },
        "payment": {
            "token": payment_token or "sandbox_default",
            "status": "sandbox_success",
            "note": "No actual charge - sandbox mode"
        },
        "fulfillment": fulfillment
    }

    ORDERS[order_id] = order
    return jsonify(order), 201


# =============================================================================
# ORDER STATUS ENDPOINTS
# =============================================================================

@ucp_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order status and details"""
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({
            "error": "Order not found",
            "order_id": order_id,
            "note": "Orders are stored in memory and reset on server restart."
        }), 404
    return jsonify(order)


@ucp_bp.route('/orders', methods=['GET'])
def list_orders():
    """List recent orders"""
    return jsonify({
        "orders": list(ORDERS.values())[-10:],
        "count": len(ORDERS),
        "sandbox": True
    })


# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@ucp_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Pudding Heroes UCP Sandbox",
        "version": "1.0.0",
        "sandbox": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@ucp_bp.route('/docs', methods=['GET'])
def docs():
    """API documentation"""
    return jsonify({
        "name": "Pudding Heroes UCP Sandbox",
        "description": "The first indie UCP merchant implementation.",
        "version": "1.0.0",
        "sandbox": True,
        "base_url": BASE_URL,
        "endpoints": {
            "GET /api/ucp/discovery": "UCP discovery manifest",
            "GET /api/ucp/products": "List products (filters: type, max_price, in_stock)",
            "GET /api/ucp/products/<id>": "Get product details",
            "POST /api/ucp/checkout": "Create an order",
            "GET /api/ucp/orders/<id>": "Get order status",
            "GET /api/ucp/test": "Quick test - creates sample order"
        },
        "free_products": ["pudding-theory-pdf", "mind-lottery", "npc-or-player"],
        "subscription_products": ["house-membership-monthly", "house-membership-annual"],
        "github": "https://github.com/steven2030/ucp-merchant"
    })


@ucp_bp.route('/examples', methods=['GET'])
def examples():
    """Code examples"""
    return jsonify({
        "curl": {
            "discovery": f"curl {BASE_URL}/.well-known/ucp.json",
            "products": f"curl {BASE_URL}/api/ucp/products",
            "checkout": f'curl -X POST {BASE_URL}/api/ucp/checkout -H "Content-Type: application/json" -d \'{{"line_items": [{{"product_id": "pudding-theory-pdf", "quantity": 1}}], "payment_token": "sandbox_test"}}\''
        },
        "python": f'''import requests

order = requests.post(
    "{BASE_URL}/api/ucp/checkout",
    json={{
        "line_items": [{{"product_id": "pudding-theory-pdf", "quantity": 1}}],
        "payment_token": "sandbox_test"
    }}
).json()

print(order["fulfillment"][0]["download_url"])'''
    })


@ucp_bp.route('/test', methods=['GET'])
def test_purchase():
    """Quick test - creates a sample order"""
    order_id = f"TEST_{uuid.uuid4().hex[:12].upper()}"

    order = {
        "order_id": order_id,
        "status": "completed",
        "sandbox": True,
        "test_mode": True,
        "message": "Test order via GET /api/ucp/test",
        "line_items": [{
            "product_id": "pudding-theory-pdf",
            "product_name": "Pudding Theory: A Guide to Warping Reality",
            "quantity": 1,
            "total": 0
        }],
        "fulfillment": [{
            "product_id": "pudding-theory-pdf",
            "type": "instant_download",
            "download_url": f"{BASE_URL}/downloads/pudding-theory.pdf",
            "status": "delivered"
        }],
        "next_steps": [
            "Download the PDF at fulfillment.download_url",
            "Try POST /api/ucp/checkout with your own data",
            "See /api/ucp/examples for code samples"
        ]
    }

    ORDERS[order_id] = order
    return jsonify(order)
