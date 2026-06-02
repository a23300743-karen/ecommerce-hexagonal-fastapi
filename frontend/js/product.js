function productImage(product) {
  if (product.image_url) return `${API_URL}${product.image_url}`;

  const value = product.name.toLowerCase();
  if (value.includes("mac")) return "img/macbook.jpg";
  if (value.includes("laptop")) return "img/laptop.jpg";
  if (value.includes("mouse")) return "img/mouse.jpg";
  if (value.includes("teclado")) return "img/teclado.jpg";
  if (value.includes("ipad") || value.includes("tablet")) return "img/ipad.jpg";
  if (value.includes("iphone") || value.includes("celular")) return "img/iphone.jpg";
  return "img/laptop.jpg";
}

function canAdmin() {
  const user = getCurrentUser();
  return user && user.role === "ADMIN";
}

async function loadProducts(query = "") {
  const path = query ? `/products/search?name=${encodeURIComponent(query)}` : "/products/";
  const products = await apiRequest(path);
  renderProducts(products);
}

function renderProducts(products) {
  const container = document.getElementById("products-list");
  container.innerHTML = "";

  if (!products.length) {
    container.innerHTML = '<p class="muted">No hay productos para mostrar.</p>';
    return;
  }

  products.forEach(product => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = `
      <img src="${productImage(product)}" alt="${product.name}">
      <div class="card-body">
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <p><strong>$${Number(product.price).toFixed(2)}</strong></p>
        <p>Stock: ${product.stock}</p>
        <span class="badge">${product.status}</span>
        ${canAdmin() ? `
          <div class="actions">
            <button onclick='editProduct(${JSON.stringify(product)})'>Editar</button>
            <button class="danger" onclick="deactivateProduct(${product.id})">Desactivar</button>
          </div>` : ""}
      </div>
    `;
    container.appendChild(card);
  });
}

function fillForm(product = null) {
  document.getElementById("product-id").value = product ? product.id : "";
  document.getElementById("name").value = product ? product.name : "";
  document.getElementById("description").value = product ? product.description : "";
  document.getElementById("price").value = product ? product.price : "";
  document.getElementById("stock").value = product ? product.stock : "";
  document.getElementById("status").value = product ? product.status : "ACTIVE";
  document.getElementById("image").value = "";
}

function editProduct(product) {
  fillForm(product);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function buildProductFormData() {
  const formData = new FormData();
  const image = document.getElementById("image").files[0];

  formData.append("name", document.getElementById("name").value);
  formData.append("description", document.getElementById("description").value);
  formData.append("price", document.getElementById("price").value);
  formData.append("stock", document.getElementById("stock").value);
  formData.append("status", document.getElementById("status").value);

  if (image) {
    formData.append("image", image);
  }

  return formData;
}

async function saveProduct(event) {
  event.preventDefault();

  const id = document.getElementById("product-id").value;

  try {
    await apiRequest(id ? `/products/${id}` : "/products/", {
      method: id ? "PUT" : "POST",
      body: buildProductFormData()
    });
    fillForm();
    showMessage("product-message", "Producto guardado correctamente.", "success");
    await loadProducts();
  } catch (error) {
    showMessage("product-message", error.message, "error");
  }
}

async function deactivateProduct(id) {
  if (!confirm("Deseas desactivar este producto?")) return;

  try {
    await apiRequest(`/products/${id}`, { method: "DELETE" });
    showMessage("product-message", "Producto desactivado.", "success");
    await loadProducts();
  } catch (error) {
    showMessage("product-message", error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const adminPanel = document.getElementById("admin-product-panel");
  if (adminPanel && !canAdmin()) adminPanel.style.display = "none";

  const form = document.getElementById("product-form");
  if (form) form.addEventListener("submit", saveProduct);

  const searchForm = document.getElementById("search-form");
  if (searchForm) {
    searchForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      await loadProducts(document.getElementById("search").value);
    });
  }

  await loadProducts();
});
