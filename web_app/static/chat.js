// chat.js
$(document).ready(function() {
    function checkTokenAndRedirect() {
        var token = getTokenFromCookie(); // 假设令牌存储在cookie中
        if (!token) {
            window.location.href = '/login'; // 如果令牌不存在，则重定向到登录页面
        }
    }

    checkTokenAndRedirect();
});

function sendMessage() {
    var userInput = $('#user-input').val().trim();
    if (!userInput) return;  // 防止發送空消息

    displayMessage(userInput, 'user-message');
    $('#user-input').val('');  // 清空輸入欄

    // 獲取token
    var token = getTokenFromCookie(); // 假設token存儲在cookie中
    $.ajax({
        url: '/chat',
        type: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: { user_message: userInput },
        success: function(response) {
            displayMessage(response, 'bot-message');
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
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
