let ws;

function connect() {
  const code = document.getElementById("sessionCode").value;
  ws = new WebSocket(`ws://${location.host}/ws/${code}`);

  ws.onmessage = (event) => {
    showMessage("assistant", event.data);
  };

  document.getElementById("login").classList.add("hidden");
  document.getElementById("chat").classList.remove("hidden");

  // Para pruebas desde consola
  window.sendMessage = (text) => {
    showMessage("user", text);
    ws.send(text);
  };
}

function showMessage(role, text) {
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.innerText = text;
  document.getElementById("messages").appendChild(div);
  document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}
