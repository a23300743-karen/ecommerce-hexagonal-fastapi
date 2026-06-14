let cartProducts = [];
function cartKey() {
  return `cart_${getCurrentUser()?.id || "guest"}`;
}
function getCart() {
  try {
    return JSON.parse(localStorage.getItem(cartKey())) || [];
  } catch {
    return [];
  }
}
function saveCart(cart) {
  localStorage.setItem(cartKey(), JSON.stringify(cart));
  renderCart();
}
function setCartProducts(products) {
  cartProducts = products;
  renderCart();
}
function addToCart(productId) {
  const product = cartProducts.find((item) => item.id === productId);
  if (!product || product.stock < 1) return;
  const cart = getCart(),
    line = cart.find((item) => item.product_id === productId);
  if (line) {
    if (line.quantity >= product.stock) {
      showMessage(
        "cart-message",
        "No puedes agregar mas unidades que el stock disponible.",
        "warning",
      );
      return;
    }
    line.quantity++;
  } else cart.push({ product_id: productId, quantity: 1 });
  saveCart(cart);
}
function changeQuantity(productId, change) {
  const cart = getCart(),
    line = cart.find((item) => item.product_id === productId),
    product = cartProducts.find((item) => item.id === productId);
  if (!line) return;
  line.quantity += change;
  if (line.quantity <= 0)
    return saveCart(cart.filter((item) => item.product_id !== productId));
  if (product && line.quantity > product.stock) {
    line.quantity = product.stock;
    showMessage(
      "cart-message",
      "Cantidad ajustada al stock disponible.",
      "warning",
    );
  }
  saveCart(cart);
}
function renderCart() {
  const container = document.getElementById("cart-items");
  if (!container) return;
  const cart = getCart();
  let total = 0,
    count = 0;
  const rows = cart
    .map((line) => {
      const product = cartProducts.find((item) => item.id === line.product_id);
      if (!product) return "";
      const subtotal = product.price * line.quantity;
      total += subtotal;
      count += line.quantity;
      return `<div class="cart-item">
        <div>
          <strong>${escapeHtml(product.name)}</strong>
          <div class="small text-secondary">${money(product.price)} c/u</div>
        </div>
        <div class="text-end">
          <div class="quantity-control">
            <button
              class="btn btn-outline-secondary btn-sm"
              onclick="changeQuantity(${product.id},-1)"
              aria-label="Reducir cantidad"
            >
              -
            </button>
            <span>${line.quantity}</span>
            <button
              class="btn btn-outline-secondary btn-sm"
              onclick="changeQuantity(${product.id},1)"
            >
              +
            </button>
          </div>
          <div class="small mt-1">${money(subtotal)}</div>
        </div>
      </div>`;
    })
    .join("");
  container.innerHTML =
    rows || '<div class="empty-state py-4">Tu carrito esta vacio.</div>';
  document.getElementById("cart-total").textContent = money(total);
  document.getElementById("cart-count").textContent = count;
  document.getElementById("checkout-button").disabled = !cart.length;
}
async function startCheckout() {
  try {
    const deployment = await getDeploymentInfo();

    if (deployment.features?.checkout_confirmation) {
      openCheckout();
      return;
    }
  } catch {
    openCheckout();
    return;
  }

  await confirmCheckout();
}

function openCheckout() {
  const cart = getCart();
  if (!cart.length) return;

  let total = 0;
  const summary = cart
    .map((line) => {
      const product = cartProducts.find((item) => item.id === line.product_id);
      if (!product) return "";

      const subtotal = product.price * line.quantity;
      total += subtotal;

      return `<div class="d-flex justify-content-between border-bottom py-2">
        <div>
          <strong>${escapeHtml(product.name)}</strong>
          <div class="small text-secondary">
            ${line.quantity} x ${money(product.price)}
          </div>
        </div>
        <span>${money(subtotal)}</span>
      </div>`;
    })
    .join("");

  document.getElementById("checkout-summary").innerHTML = summary;
  document.getElementById("checkout-total").textContent = money(total);
  document.getElementById("checkout-message").innerHTML = "";

  bootstrap.Modal.getOrCreateInstance("#checkout-modal").show();
}

async function confirmCheckout() {
  const cart = getCart();
  if (!cart.length) return;

  const button = document.getElementById("confirm-checkout-button");
  button.disabled = true;
  button.textContent = "Confirmando...";

  try {
    const order = await apiRequest("/orders/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: cart }),
    });

    localStorage.removeItem(cartKey());
    bootstrap.Modal.getOrCreateInstance("#checkout-modal").hide();
    showMessage(
      "cart-message",
      `Compra realizada. Orden #${order.id}`,
      "success",
    );
    await loadProducts();
    renderCart();
  } catch (error) {
    showMessage("checkout-message", error.message, "error");
  } finally {
    button.disabled = false;
    button.textContent = "Confirmar compra";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("checkout-button")
    ?.addEventListener("click", startCheckout);
  document
    .getElementById("confirm-checkout-button")
    ?.addEventListener("click", confirmCheckout);
});
