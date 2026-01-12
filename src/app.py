"""
Pudding Heroes UCP Merchant
The first open-source UCP (Universal Commerce Protocol) implementation.

Run locally:
    python src/app.py

Test:
    curl http://localhost:5000/api/ucp/health
"""

from flask import Flask
from flask_cors import CORS
from routes import ucp_bp

app = Flask(__name__)
CORS(app)

# Register UCP blueprint
app.register_blueprint(ucp_bp)

# Also serve discovery at root .well-known
@app.route('/.well-known/ucp.json')
def wellknown_discovery():
    from routes import discovery
    return discovery()

if __name__ == '__main__':
    print("=" * 60)
    print("Pudding Heroes UCP Merchant Sandbox")
    print("=" * 60)
    print("")
    print("Endpoints:")
    print("  Discovery:  http://localhost:5000/.well-known/ucp.json")
    print("  Products:   http://localhost:5000/api/ucp/products")
    print("  Checkout:   http://localhost:5000/api/ucp/checkout")
    print("  Docs:       http://localhost:5000/api/ucp/docs")
    print("  Test:       http://localhost:5000/api/ucp/test")
    print("")
    print("Live sandbox: https://puddingheroes.com/api/ucp/")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True)
