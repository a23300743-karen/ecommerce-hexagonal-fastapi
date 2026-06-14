let adminProducts = [];
let productModal;
let orderModal;
let adminChatSocket;
let selectedConversationId = null;
document.addEventListener("DOMContentLoaded", () => {
  if (!requireRole("ADMIN")) return;
  productModal = new bootstrap.Modal("#product-modal");
  orderModal = new bootstrap.Modal("#order-modal");
  document
    .getElementById("product-form")
    .addEventListener("submit", saveProduct);
  document
    .getElementById("new-product-button")
    .addEventListener("click", resetProductForm);
  document
    .getElementById("reload-admin-orders")
    .addEventListener("click", loadAdminOrders);
  document
    .getElementById("admin-chat-form")
    .addEventListener("submit", sendAdminMessage);
  connectAdminChat();
  loadAdminProducts();
  loadAdminOrders();
  loadConversations();
});
async function loadAdminProducts() {
  try {
    adminProducts = await apiRequest("/products/");
    document.getElementById("admin-products").innerHTML = adminProducts
      .map(
        (product) =>
          `<tr>
            <td>
              ${
                product.image_url
                  ? `<img src="${productImage(product.image_url)}" alt="">`
                  : "Sin imagen"
              }
            </td>
            <td>
              <strong>${escapeHtml(product.name)}</strong>
              <div class="small text-secondary">
                ${escapeHtml(product.description)}
              </div>
            </td>
            <td>${money(product.price)}</td>
            <td>${product.stock}</td>
            <td>
              <span
                class="badge ${
                  product.status === "ACTIVE"
                    ? "text-bg-success"
                    : "text-bg-secondary"
                }"
              >
                ${product.status}
              </span>
            </td>
            <td class="text-end">
              <button
                class="btn btn-outline-primary btn-sm"
                onclick="editProduct(${product.id})"
                data-bs-toggle="modal"
                data-bs-target="#product-modal"
              >
                Editar
              </button>
              <button
                class="btn btn-outline-danger btn-sm"
                onclick="deactivateProduct(${product.id})"
                ${product.status === "INACTIVE" ? "disabled" : ""}
              >
                Desactivar
              </button>
            </td>
          </tr>`,
      )
      .join("");
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
function resetProductForm() {
  document.getElementById("product-form").reset();
  document.getElementById("product-id").value = "";
  document.getElementById("product-modal-title").textContent = "Nuevo producto";
}
function editProduct(id) {
  const p = adminProducts.find((item) => item.id === id);
  document.getElementById("product-id").value = p.id;
  document.getElementById("admin-name").value = p.name;
  document.getElementById("admin-description").value = p.description;
  document.getElementById("admin-price").value = p.price;
  document.getElementById("admin-stock").value = p.stock;
  document.getElementById("admin-status").value = p.status;
  document.getElementById("admin-image").value = "";
  document.getElementById("product-modal-title").textContent =
    `Editar ${p.name}`;
}
async function saveProduct(event) {
  event.preventDefault();
  const id = document.getElementById("product-id").value,
    form = new FormData();
  form.append("name", document.getElementById("admin-name").value.trim());
  form.append(
    "description",
    document.getElementById("admin-description").value.trim(),
  );
  form.append("price", document.getElementById("admin-price").value);
  form.append("stock", document.getElementById("admin-stock").value);
  form.append("status", document.getElementById("admin-status").value);
  const image = document.getElementById("admin-image").files[0];
  if (image) form.append("image", image);
  try {
    await apiRequest(id ? `/products/${id}` : "/products/", {
      method: id ? "PUT" : "POST",
      body: form,
    });
    productModal.hide();
    showMessage("admin-message", "Producto guardado correctamente.", "success");
    loadAdminProducts();
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
async function deactivateProduct(id) {
  if (!confirm("Desactivar este producto? Ya no aparecera en la tienda."))
    return;
  try {
    await apiRequest(`/products/${id}`, { method: "DELETE" });
    loadAdminProducts();
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
async function loadAdminOrders() {
  try {
    const orders = await apiRequest("/orders/");
    document.getElementById("admin-orders").innerHTML =
      orders
        .map(
          (order) =>
            `<tr>
              <td>#${order.id}</td>
              <td>
                ${escapeHtml(order.buyer_name || `Perfil #${order.buyer_id}`)}
              </td>
              <td>${money(order.total)}</td>
              <td>
                <span
                  class="badge ${
                    order.status === "CANCELLED"
                      ? "text-bg-secondary"
                      : "text-bg-success"
                  }"
                >
                  ${order.status}
                </span>
              </td>
              <td class="text-end">
                <button
                  class="btn btn-outline-primary btn-sm"
                  onclick="showOrder(${order.id})"
                >
                  Ver detalle
                </button>
                ${
                  order.status !== "CANCELLED"
                    ? `<button
                        class="btn btn-outline-danger btn-sm"
                        onclick="adminCancelOrder(${order.id})"
                      >
                        Cancelar
                      </button>`
                    : ""
                }
              </td>
            </tr>`,
        )
        .join("") ||
      '<tr><td colspan="5" class="empty-state">No hay ordenes.</td></tr>';
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
async function showOrder(id) {
  try {
    const items = await apiRequest(`/orders/${id}/items`);
    document.getElementById("admin-order-detail").innerHTML =
      items
        .map(
          (item) =>
            `<div class="d-flex justify-content-between border-bottom py-2">
              <span>
                ${escapeHtml(
                  item.product_name || `Producto #${item.product_id}`,
                )}
                <br>
                <small>
                  ${item.quantity} x ${money(item.unit_price)}
                </small>
              </span>
              <strong>${money(item.subtotal)}</strong>
            </div>`,
        )
        .join("") || "Sin productos";
    orderModal.show();
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
async function adminCancelOrder(id) {
  if (!confirm("Cancelar la orden y devolver su stock?")) return;
  try {
    await apiRequest(`/orders/${id}/cancel`, { method: "PATCH" });
    loadAdminOrders();
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
function connectAdminChat() {
  adminChatSocket = new WebSocket(
    `${WS_URL}?token=${encodeURIComponent(getAccessToken())}`,
  );
  adminChatSocket.onopen = () =>
    (document.getElementById("admin-chat-status").textContent = "En linea");
  adminChatSocket.onclose = () =>
    (document.getElementById("admin-chat-status").textContent = "Desconectado");
  adminChatSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "conversation_updated") {
      loadConversations();
      if (data.conversation_id === selectedConversationId)
        selectConversation(selectedConversationId);
    } else if (
      data.type === "message" &&
      data.message.conversation_id === selectedConversationId
    ) {
      appendAdminMessage(data.message);
    }
  };
}
async function loadConversations() {
  try {
    const conversations = await apiRequest("/support/conversations");
    document.getElementById("conversation-list").innerHTML =
      conversations
        .map(
          (item) =>
            `<button
              class="list-group-item list-group-item-action ${
                item.id === selectedConversationId ? "active" : ""
              }"
              onclick="selectConversation(${item.id})"
            >
              <strong>${escapeHtml(item.user_name)}</strong>
              <br>
              <small>Conversacion #${item.id} - ${item.status}</small>
            </button>`,
        )
        .join("") ||
      '<div class="empty-state border">Sin conversaciones.</div>';
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
async function selectConversation(id, name) {
  selectedConversationId = id;
  document.getElementById("conversation-title").textContent = name
    ? `Conversacion con ${name}`
    : `Conversacion #${id}`;
  document.getElementById("admin-chat-input").disabled = false;
  document.getElementById("admin-chat-send").disabled = false;
  try {
    const messages = await apiRequest(`/support/conversations/${id}/messages`);
    const box = document.getElementById("admin-chat-box");
    box.innerHTML = "";
    messages.forEach(appendAdminMessage);
    loadConversations();
  } catch (error) {
    showMessage("admin-message", error.message, "error");
  }
}
function appendAdminMessage(message) {
  const box = document.getElementById("admin-chat-box"),
    bubble = document.createElement("div");
  bubble.className = `chat-bubble ${message.sender_role === "CUSTOMER" ? "user" : "assistant"}`;
  bubble.textContent = `${message.sender_role}: ${message.content}`;
  box.appendChild(bubble);
  box.scrollTop = box.scrollHeight;
}
function sendAdminMessage(event) {
  event.preventDefault();
  const input = document.getElementById("admin-chat-input"),
    content = input.value.trim();
  if (
    !selectedConversationId ||
    !content ||
    adminChatSocket?.readyState !== WebSocket.OPEN
  )
    return;
  adminChatSocket.send(
    JSON.stringify({ conversation_id: selectedConversationId, content }),
  );
  input.value = "";
}
