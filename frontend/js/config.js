const API_URL = "http://127.0.0.1:8000";
const WS_URL = "ws://127.0.0.1:8000/ws/chat";

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

function saveTokens(data) {
  localStorage.setItem("access_token", data.access_token);
  if (data.refresh_token) {
    localStorage.setItem("refresh_token", data.refresh_token);
  }
}

function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("current_user");
}

function getCurrentUser() {
  const raw = localStorage.getItem("current_user");
  return raw ? JSON.parse(raw) : null;
}

function setCurrentUser(user) {
  localStorage.setItem("current_user", JSON.stringify(user));
}

async function apiRequest(path, options = {}) {
  const headers = options.headers || {};
  const token = getAccessToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message = data && data.detail ? data.detail : "Error en la peticion";
    throw new Error(message);
  }

  return data;
}

function showMessage(id, message, type = "notice") {
  const element = document.getElementById(id);
  if (!element) return;
  element.className = `notice ${type}`;
  element.textContent = message;
}

function logout() {
  clearSession();
  window.location.href = "login.html";
}

function renderNav() {
  const user = getCurrentUser();
  const container = document.getElementById("session-info");
  if (!container) return;

  if (!user) {
    container.innerHTML = '<span class="muted">Sin sesion</span>';
    return;
  }

  container.innerHTML = `<span>${user.name} (${user.role})</span> <button onclick="logout()">Salir</button>`;
}

document.addEventListener("DOMContentLoaded", renderNav);
