let visibleProducts = [];
document.addEventListener("DOMContentLoaded", () => {
  if (!requireRole("CUSTOMER")) return;
  document
    .getElementById("search-form")
    ?.addEventListener("submit", searchProducts);
  loadProducts();
});
async function loadProducts(path = "/products/") {
  try {
    const products = await apiRequest(path);
    visibleProducts = products.filter(
      (product) => product.status === "ACTIVE" && product.stock > 0,
    );
    setCartProducts(visibleProducts);
    renderProducts();
  } catch (error) {
    showMessage("products-message", error.message, "error");
  }
}
async function searchProducts(event) {
  event.preventDefault();
  const value = document.getElementById("product-search").value.trim();
  loadProducts(
    value ? `/products/search?name=${encodeURIComponent(value)}` : "/products/",
  );
}
function renderProducts() {
  const grid = document.getElementById("product-grid");
  grid.innerHTML =
    visibleProducts
      .map(
        (product) =>
          `<div class="col-sm-6 col-lg-4">
            <article class="card product-card">
              <div class="${product.image_url ? "" : "product-placeholder"}">
                ${
                  product.image_url
                    ? `<img
                        class="product-image"
                        src="${productImage(product.image_url)}"
                        alt="${escapeHtml(product.name)}"
                      >`
                    : `<div class="product-image product-placeholder">
                        Sin imagen
                      </div>`
                }
              </div>
              <div class="card-body d-flex flex-column">
                <h2 class="h5">${escapeHtml(product.name)}</h2>
                <p class="text-secondary small flex-grow-1">
                  ${escapeHtml(product.description)}
                </p>
                <div class="d-flex justify-content-between align-items-end">
                  <div>
                    <strong class="fs-5">${money(product.price)}</strong>
                    <div class="small text-secondary">
                      ${product.stock} disponibles
                    </div>
                  </div>
                  <button
                    class="btn btn-primary btn-sm"
                    onclick="addToCart(${product.id})"
                  >
                    Agregar
                  </button>
                </div>
              </div>
            </article>
          </div>`,
      )
      .join("") ||
    '<div class="col-12 empty-state">No se encontraron productos disponibles.</div>';
}
