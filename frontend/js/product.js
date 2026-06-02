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
    container.innerHTML = '<div class="col-12"><div class="alert alert-secondary">No hay productos para mostrar.</div></div>';
    return;
  }

  products.forEach(product => {
    const column = document.createElement("div");
    column.className = "col-sm-6 col-lg-4";
    const statusClass = product.status === "ACTIVE" ? "success" : "secondary";
    column.innerHTML = `
      <article class="card h-100 shadow-sm border-0">
        <img class="product-image card-img-top" src="${productImage(product)}" alt="${product.name}">
        <div class="card-body d-flex flex-column">
          <div class="d-flex justify-content-between gap-2 align-items-start">
            <h3 class="h5 card-title">${product.name}</h3>
            <span class="badge text-bg-${statusClass}">${product.status}</span>
          </div>
          <p class="card-text text-secondary">${product.description}</p>
          <p class="h5 mb-1">$${Number(product.price).toFixed(2)}</p>
          <p class="small text-secondary">Stock: ${product.stock}</p>
          ${canAdmin() ? `
            <div class="d-flex gap-2 mt-auto">
              <button class="btn btn-outline-primary btn-sm" onclick='editProduct(${JSON.stringify(product)})'>Editar</button>
              <button class="btn btn-outline-danger btn-sm" onclick="deactivateProduct(${product.id})">Desactivar</button>
            </div>` : ""}
        </div>
      </article>
    `;
    container.appendChild(column);
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
