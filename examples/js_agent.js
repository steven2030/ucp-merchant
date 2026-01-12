/**
 * Example UCP Agent in JavaScript
 *
 * Demonstrates a complete shopping flow:
 * 1. Discover merchant capabilities
 * 2. Browse products
 * 3. Make a purchase
 * 4. Check order status
 */

const BASE_URL = "https://puddingheroes.com"; // Or http://localhost:5000 for local

async function main() {
  console.log("=".repeat(60));
  console.log("UCP Agent Demo (JavaScript)");
  console.log("=".repeat(60));

  // Step 1: Discovery
  console.log("\n[1] Discovering merchant...");
  const discovery = await fetch(`${BASE_URL}/.well-known/ucp.json`).then(r => r.json());
  const merchant = discovery.ucp.merchant;
  console.log(`    Merchant: ${merchant.name}`);
  console.log(`    Description: ${merchant.description}`);
  console.log(`    Sandbox mode: ${discovery.ucp.sandbox}`);

  // Step 2: List products
  console.log("\n[2] Fetching product catalog...");
  const products = await fetch(`${BASE_URL}/api/ucp/products`).then(r => r.json());
  console.log(`    Found ${products.count} products:`);
  for (const p of products.products) {
    console.log(`    - ${p.name}: $${p.price} (${p.type})`);
  }

  // Step 3: Get free products
  console.log("\n[3] Finding free products...");
  const freeProducts = await fetch(`${BASE_URL}/api/ucp/products?max_price=0`).then(r => r.json());
  console.log(`    Found ${freeProducts.count} free items`);

  // Step 4: Make a purchase
  console.log("\n[4] Purchasing 'Pudding Theory' PDF...");
  const order = await fetch(`${BASE_URL}/api/ucp/checkout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      line_items: [{ product_id: "pudding-theory-pdf", quantity: 1 }],
      buyer: { name: "JavaScript Agent", email: "agent@example.com" },
      payment_token: "sandbox_test"
    })
  }).then(r => r.json());

  console.log(`    Order ID: ${order.order_id}`);
  console.log(`    Status: ${order.status}`);
  console.log(`    Total: $${order.totals.total}`);

  // Step 5: Get download link
  if (order.fulfillment && order.fulfillment.length > 0) {
    const fulfillment = order.fulfillment[0];
    console.log("\n[5] Fulfillment:");
    console.log(`    Type: ${fulfillment.type}`);
    console.log(`    Status: ${fulfillment.status}`);
    if (fulfillment.download_url) {
      console.log(`    Download URL: ${fulfillment.download_url}`);
    }
  }

  // Step 6: Check order status
  console.log("\n[6] Checking order status...");
  const orderStatus = await fetch(`${BASE_URL}/api/ucp/orders/${order.order_id}`).then(r => r.json());
  console.log(`    Order ${orderStatus.order_id}: ${orderStatus.status}`);

  console.log("\n" + "=".repeat(60));
  console.log("Demo complete!");
  console.log("=".repeat(60));
}

main().catch(console.error);
