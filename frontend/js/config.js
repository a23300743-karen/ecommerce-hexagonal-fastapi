const STATIC_SERVER_PORTS = ["5500", "5501"];
const USE_LOCAL_BACKEND = STATIC_SERVER_PORTS.includes(location.port);
const API_URL = USE_LOCAL_BACKEND
  ? "http://127.0.0.1:8000"
  : window.location.origin;
const WS_PROTOCOL = window.location.protocol === "https:" ? "wss:" : "ws:";
const WS_URL = USE_LOCAL_BACKEND
  ? "ws://127.0.0.1:8000/ws/chat"
  : `${WS_PROTOCOL}//${window.location.host}/ws/chat`;
function getAccessToken() {
  return localStorage.getItem("access_token");
}
function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}
function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem("current_user"));
  } catch {
    return null;
  }
}
function setCurrentUser(user) {
  localStorage.setItem("current_user", JSON.stringify(user));
}
function saveTokens(data) {
  localStorage.setItem("access_token", data.access_token);
  if (data.refresh_token)
    localStorage.setItem("refresh_token", data.refresh_token);
}
function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("current_user");
}
function logout() {
  clearSession();
  location.href = "login.html";
}
async function refreshSession() {
  const token = getRefreshToken();
  if (!token) return false;
  const response = await fetch(`${API_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: token }),
  });
  if (!response.ok) return false;
  saveTokens(await response.json());
  return true;
}
async function apiRequest(path, options = {}, retry = true) {
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (response.status === 401 && retry && !path.startsWith("/auth/")) {
    if (await refreshSession()) return apiRequest(path, options, false);
    clearSession();
    location.href = "login.html";
    throw new Error("Tu sesion termino. Inicia sesion otra vez.");
  }
  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!response.ok)
    throw new Error(data?.detail || "No fue posible completar la solicitud");
  return data;
}
function showMessage(id, message, type = "info") {
  const element = document.getElementById(id);
  if (!element) return;
  element.className = `alert alert-${type === "error" ? "danger" : type} mt-3`;
  element.textContent = message;
}
function money(value) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
  }).format(value);
}
function productImage(url) {
  return url ? `${API_URL}${url}` : "";
}
function requireRole(role) {
  const user = getCurrentUser();
  if (!user) {
    location.replace("login.html");
    return null;
  }
  if (role && user.role !== role) {
    location.replace(user.role === "ADMIN" ? "admin.html" : "products.html");
    return null;
  }
  return user;
}
function renderNav() {
  const container = document.getElementById("session-info"),
    user = getCurrentUser();
  if (!container) return;
  container.innerHTML = user
    ? `<span class="navbar-text text-white small">
        ${escapeHtml(user.name)} | ${user.role}
      </span>
      <button class="btn btn-outline-light btn-sm" onclick="logout()">
        Salir
      </button>`
    : "";
}
function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = String(value ?? "");
  return div.innerHTML;
}
document.addEventListener("DOMContentLoaded", renderNav);

let deploymentInfoPromise;

async function getDeploymentInfo() {
  if (!deploymentInfoPromise) {
    deploymentInfoPromise = fetch(`${API_URL}/deployment`).then((response) => {
      if (!response.ok) throw new Error("Deployment info unavailable");
      return response.json();
    });
  }

  return deploymentInfoPromise;
}

async function renderDeploymentIndicator() {
  try {
    const deployment = await getDeploymentInfo();
    const environment = deployment.environment?.toUpperCase();
    const indicator = document.createElement("div");
    const color = environment === "GREEN" ? "success" : "primary";

    indicator.className = `deployment-indicator badge text-bg-${color}`;
    indicator.textContent = `${environment} | ${deployment.version}`;
    indicator.title = deployment.message;
    document.body.appendChild(indicator);

    if (environment === "GREEN") {
      document.body.classList.add("deployment-green");
      renderGreenReleaseBanner(deployment);
    }
  } catch {
    // El indicador no interrumpe la aplicacion si el backend no esta disponible.
  }
}

function renderGreenReleaseBanner(deployment) {
  const main = document.querySelector("main");
  if (!main || document.getElementById("green-release-banner")) return;

  const banner = document.createElement("div");
  banner.id = "green-release-banner";
  banner.className = "green-release-banner";
  banner.innerHTML = `
    <div>
      <strong>Estas probando Green ${escapeHtml(deployment.version)}</strong>
      <span>${escapeHtml(deployment.message)}</span>
    </div>
    <span class="green-release-feature">Nuevo: confirma tu compra antes de crear la orden</span>
  `;
  main.prepend(banner);
}

document.addEventListener("DOMContentLoaded", renderDeploymentIndicator);
