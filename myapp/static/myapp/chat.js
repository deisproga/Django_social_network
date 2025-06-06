document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.querySelector(".chat-box");
    const toggleBtn = document.querySelector("#chat-toggle-btn");
    const messageInput = document.querySelector("#chat-message-input");
    const messagesContainer = document.querySelector("#chat-messages");

    toggleBtn.addEventListener("click", () => {
        if (chatBox.style.display === "none" || !chatBox.style.display) {
            chatBox.style.display = "block";
        } else {
            chatBox.style.display = "none";
        }
    });

    // Подключение к WebSocket (пример для chat_id = 1)
    const chatId = 1;  // менять динамически по нужде
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/${chatId}/`);

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const newMessage = document.createElement("div");
        newMessage.textContent = `${data.sender}: ${data.message}`;
        messagesContainer.appendChild(newMessage);
    };

    messageInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && messageInput.value.trim() !== "") {
            socket.send(JSON.stringify({
                "message": messageInput.value
            }));
            messageInput.value = "";
        }
    });
});