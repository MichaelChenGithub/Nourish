// script.js
function sendMessage() {
    var userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return;  // Prevent sending empty messages

    displayMessage(userInput, 'user-message');
    document.getElementById('user-input').value = '';  // Clear input field
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chat', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = xhr.responseText;
            displayMessage(response, 'bot-message');
        }
    };
    xhr.send('user_message=' + encodeURIComponent(userInput));
}

function setInput(question) {
    document.getElementById('user-input').value = question;
    sendMessage(); // 假設您已有此函數處理消息發送
}

function displayMessage(message, className) {
    var chatDisplay = document.getElementById('chat-display');
    var messageElement = document.createElement('p');
    messageElement.className = className;
    messageElement.innerHTML = '<pre>' + message + '</pre>';
    chatDisplay.appendChild(messageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;  // Scroll to the bottom
}

// Listen for the Enter key press on the input field
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
