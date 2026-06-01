let socket = null;

function addMessage(data, className = "") {
  const box = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = `message ${className || data.type || ""}`;
  const content = data.message ? `<p><strong>${data.message.user}:</strong> ${data.message.content}</p>` : "";
  div.innerHTML = `${content}<p>${data.response}</p><small>${data.type}</small>`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function connectChat() {
  socket = new WebSocket(WS_URL);

  socket.onopen = () => showMessage("chat-status", "Conectado al chat.", "success");
  socket.onclose = () => showMessage("chat-status", "Conexion cerrada.", "error");
  socket.onerror = () => showMessage("chat-status", "Error de conexion WebSocket.", "error");

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addMessage(data);
  };
}

function sendChatMessage(event) {
  event.preventDefault();

  const input = document.getElementById("chat-message");
  const content = input.value.trim();
  if (!content || !socket || socket.readyState !== WebSocket.OPEN) return;

  const user = getCurrentUser();
  socket.send(JSON.stringify({
    user: user ? user.name : "client",
    content
  }));

  input.value = "";
}

document.addEventListener("DOMContentLoaded", () => {
  connectChat();
  document.getElementById("chat-form").addEventListener("submit", sendChatMessage);
});
