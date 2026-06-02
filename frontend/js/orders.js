async function loadBuyers() {
  const buyers = await apiRequest("/buyers/");
  const select = document.getElementById("buyer-id");
  if (!select) return;
  select.innerHTML = buyers.map(b => `<option value="${b.id}">${b.name} - ${b.email}</option>`).join("");
}

async function loadProductsForOrders() {
  const products = await apiRequest("/products/");
  const select = document.getElementById("product-id");
  if (!select) return;
  select.innerHTML = products
    .filter(p => p.status === "ACTIVE")
    .map(p => `<option value="${p.id}">${p.name} ($${Number(p.price).toFixed(2)}) - stock ${p.stock}</option>`)
    .join("");
}

async function loadOrders() {
  const orders = await apiRequest("/orders/");
  const container = document.getElementById("orders-list");
  container.innerHTML = "";

  if (!orders.length) {
    container.innerHTML = '<div class="col-12"><div class="alert alert-secondary">No hay ordenes.</div></div>';
    return;
  }

  orders.forEach(order => {
    const column = document.createElement("div");
    column.className = "col-md-6 col-lg-4";
    const statusClass = order.status === "CANCELLED" ? "secondary" : "success";
    column.innerHTML = `
      <article class="card h-100 shadow-sm border-0">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h3 class="h5">Orden #${order.id}</h3>
            <span class="badge text-bg-${statusClass}">${order.status}</span>
          </div>
          <p class="mb-1 text-secondary">Buyer ID: ${order.buyer_id}</p>
          <p class="h5">$${Number(order.total).toFixed(2)}</p>
          <div class="d-flex gap-2 mb-3">
            <button class="btn btn-outline-primary btn-sm" onclick="viewItems(${order.id})">Ver items</button>
            <button class="btn btn-outline-danger btn-sm" onclick="cancelOrder(${order.id})">Cancelar</button>
          </div>
          <div id="items-${order.id}" class="small text-secondary"></div>
        </div>
      </article>
    `;
    container.appendChild(column);
  });
}

async function createBuyer(event) {
  event.preventDefault();

  const payload = {
    name: document.getElementById("buyer-name").value,
    email: document.getElementById("buyer-email").value,
    address: document.getElementById("buyer-address").value,
    phone: document.getElementById("buyer-phone").value || null
  };

  try {
    await apiRequest("/buyers/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    showMessage("order-message", "Comprador creado.", "success");
    event.target.reset();
    await loadBuyers();
  } catch (error) {
    showMessage("order-message", error.message, "error");
  }
}

async function createOrder(event) {
  event.preventDefault();

  const payload = {
    buyer_id: Number(document.getElementById("buyer-id").value),
    product_id: Number(document.getElementById("product-id").value),
    quantity: Number(document.getElementById("quantity").value)
  };

  try {
    await apiRequest("/orders/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    showMessage("order-message", "Orden creada.", "success");
    await loadOrders();
    await loadProductsForOrders();
  } catch (error) {
    showMessage("order-message", error.message, "error");
  }
}

async function viewItems(orderId) {
  try {
    const items = await apiRequest(`/orders/${orderId}/items`);
    const container = document.getElementById(`items-${orderId}`);
    container.innerHTML = items.map(item => `<div class="border-top py-1">Producto ${item.product_id}: ${item.quantity} x $${Number(item.unit_price).toFixed(2)}</div>`).join("");
  } catch (error) {
    showMessage("order-message", error.message, "error");
  }
}

async function cancelOrder(orderId) {
  if (!confirm("Deseas cancelar esta orden?")) return;

  try {
    await apiRequest(`/orders/${orderId}/cancel`, { method: "PATCH" });
    showMessage("order-message", "Orden cancelada.", "success");
    await loadOrders();
    await loadProductsForOrders();
  } catch (error) {
    showMessage("order-message", error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const buyerForm = document.getElementById("buyer-form");
  const orderForm = document.getElementById("order-form");

  if (buyerForm) buyerForm.addEventListener("submit", createBuyer);
  if (orderForm) orderForm.addEventListener("submit", createOrder);

  try {
    await loadBuyers();
    await loadProductsForOrders();
    await loadOrders();
  } catch (error) {
    showMessage("order-message", error.message, "error");
  }
});
