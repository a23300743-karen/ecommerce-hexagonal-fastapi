document.addEventListener("DOMContentLoaded", () => {
  const existing = getCurrentUser();
  if (existing && location.pathname.endsWith("login.html"))
    location.replace(
      existing.role === "ADMIN" ? "admin.html" : "products.html",
    );
  document.getElementById("login-form")?.addEventListener("submit", login);
  document
    .getElementById("register-form")
    ?.addEventListener("submit", register);
});
async function login(event) {
  event.preventDefault();
  const button = document.getElementById("login-button");
  if (button) button.disabled = true;
  const body = new URLSearchParams();
  body.set("username", document.getElementById("email").value.trim());
  body.set("password", document.getElementById("password").value);
  try {
    const tokens = await apiRequest("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    saveTokens(tokens);
    const user = await apiRequest("/auth/me");
    setCurrentUser(user);
    location.href = user.role === "ADMIN" ? "admin.html" : "products.html";
  } catch (error) {
    showMessage("auth-message", error.message, "error");
  } finally {
    if (button) button.disabled = false;
  }
}
async function register(event) {
  event.preventDefault();
  const payload = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    password: document.getElementById("password").value,
    role: "CUSTOMER",
    address: document.getElementById("address").value.trim(),
    phone: document.getElementById("phone").value.trim() || null,
  };
  try {
    await apiRequest("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    showMessage(
      "auth-message",
      "Cuenta creada. Te llevaremos al inicio de sesion.",
      "success",
    );
    setTimeout(() => (location.href = "login.html"), 1200);
  } catch (error) {
    showMessage("auth-message", error.message, "error");
  }
}
