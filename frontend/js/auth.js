async function register(event) {
  event.preventDefault();

  const payload = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    role: document.getElementById("role").value
  };

  try {
    await apiRequest("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    showMessage("auth-message", "Usuario registrado. Ahora inicia sesion.", "success");
  } catch (error) {
    showMessage("auth-message", error.message, "error");
  }
}

async function login(event) {
  event.preventDefault();

  const formData = new FormData();
  formData.append("username", document.getElementById("email").value);
  formData.append("password", document.getElementById("password").value);

  try {
    const tokens = await apiRequest("/auth/login", {
      method: "POST",
      body: formData
    });

    saveTokens(tokens);
    const user = await apiRequest("/auth/me");
    setCurrentUser(user);
    window.location.href = "products.html";
  } catch (error) {
    showMessage("auth-message", error.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  if (registerForm) registerForm.addEventListener("submit", register);
  if (loginForm) loginForm.addEventListener("submit", login);
});
