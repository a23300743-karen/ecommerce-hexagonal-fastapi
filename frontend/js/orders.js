document.addEventListener("DOMContentLoaded", () => {
  if (!requireRole("CUSTOMER")) return;
  document
    .getElementById("reload-orders")
    ?.addEventListener("click", loadOrders);
  loadOrders();
});
async function loadOrders() {
  try {
    const orders = await apiRequest("/orders/me");
    const list = document.getElementById("orders-list");
    list.innerHTML =
      orders
        .map(
          (order) =>
            `<article class="accordion-item">
              <h2 class="accordion-header">
                <button
                  class="accordion-button collapsed"
                  data-bs-toggle="collapse"
                  data-bs-target="#order-${order.id}"
                  onclick="loadOrderItems(${order.id})"
                >
                  <span class="me-3">Orden #${order.id}</span>
                  <span
                    class="badge ${
                      order.status === "CANCELLED"
                        ? "text-bg-secondary"
                        : "text-bg-success"
                    } me-3"
                  >
                    ${order.status}
                  </span>
                  <strong>${money(order.total)}</strong>
                </button>
              </h2>
              <div id="order-${order.id}" class="accordion-collapse collapse">
                <div class="accordion-body">
                  <div id="items-${order.id}">Cargando productos...</div>
                  ${
                    order.status !== "CANCELLED"
                      ? `<button
                          class="btn btn-outline-danger btn-sm mt-3"
                          onclick="cancelOrder(${order.id})"
                        >
                          Cancelar orden
                        </button>`
                      : ""
                  }
                </div>
              </div>
            </article>`,
        )
        .join("") ||
      '<div class="empty-state bg-white border">Todavia no tienes compras.</div>';
  } catch (error) {
    showMessage("orders-message", error.message, "error");
  }
}
async function loadOrderItems(id) {
  const container = document.getElementById(`items-${id}`);
  if (container.dataset.loaded) return;
  try {
    const items = await apiRequest(`/orders/me/${id}/items`);
    container.innerHTML = items
      .map(
        (item) =>
          `<div class="d-flex justify-content-between border-bottom py-2">
            <span>
              ${escapeHtml(item.product_name || `Producto #${item.product_id}`)}
              x ${item.quantity} unidad(es)
            </span>
            <span>${money(item.subtotal)}</span>
          </div>`,
      )
      .join("");
    container.dataset.loaded = "true";
  } catch (error) {
    container.textContent = error.message;
  }
}
async function cancelOrder(id) {
  if (!confirm("Deseas cancelar esta orden? El stock sera devuelto.")) return;
  try {
    await apiRequest(`/orders/${id}/cancel`, { method: "PATCH" });
    loadOrders();
  } catch (error) {
    showMessage("orders-message", error.message, "error");
  }
}
