let chatSocket;
document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("chat-form")) return;
  connectChat();
  document
    .getElementById("chat-form")
    .addEventListener("submit", sendChatMessage);
});
function connectChat() {
  chatSocket = new WebSocket(
    `${WS_URL}?token=${encodeURIComponent(getAccessToken())}`,
  );
  chatSocket.onopen = () =>
    (document.getElementById("chat-status").textContent = "Soporte conectado");
  chatSocket.onmessage = (event) => handleChatPayload(JSON.parse(event.data));
  chatSocket.onclose = () =>
    (document.getElementById("chat-status").textContent =
      "Soporte desconectado");
  chatSocket.onerror = () =>
    (document.getElementById("chat-status").textContent =
      "No se pudo conectar");
}
function handleChatPayload(data) {
  if (data.type === "history") {
    document.getElementById("chat-box").innerHTML = "";
    data.messages.forEach((message) =>
      appendChat(
        message.content,
        message.sender_role === "CUSTOMER" ? "user" : "assistant",
      ),
    );
    return;
  }
  if (data.type === "message")
    appendChat(
      data.message.content,
      data.message.sender_role === "CUSTOMER" ? "user" : "assistant",
    );
  if (data.type === "error") appendChat(data.response, "assistant");
}
function sendChatMessage(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input"),
    content = input.value.trim();
  if (!content || chatSocket?.readyState !== WebSocket.OPEN) return;
  appendChat(content, "user");
  chatSocket.send(JSON.stringify({ content }));
  input.value = "";
}
function appendChat(text, type) {
  const box = document.getElementById("chat-box"),
    bubble = document.createElement("div");
  bubble.className = `chat-bubble ${type}`;
  bubble.textContent = text;
  box.appendChild(bubble);
  box.scrollTop = box.scrollHeight;
}
