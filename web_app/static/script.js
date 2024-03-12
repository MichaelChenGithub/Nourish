// script.js
// 從 cookie 中獲取 token
function getTokenFromCookie() {
    var name = "token=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i].trim();
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

// function sendMessage() {
//     var userInput = document.getElementById('user-input').value.trim();
//     if (!userInput) return;  // Prevent sending empty messages

//     displayMessage(userInput, 'user-message');
//     document.getElementById('user-input').value = '';  // Clear input field
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/chat', true);
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             var response = xhr.responseText;
//             displayMessage(response, 'bot-message');
//         }
//     };
//     xhr.send('user_message=' + encodeURIComponent(userInput));
// }

// function setInput(question) {
//     document.getElementById('user-input').value = question;
//     sendMessage(); // 假設您已有此函數處理消息發送
// }

// function displayMessage(message, className) {
//     var chatDisplay = document.getElementById('chat-display');
//     var messageElement = document.createElement('p');
//     messageElement.className = className;
//     messageElement.innerHTML = '<pre>' + message + '</pre>';
//     chatDisplay.appendChild(messageElement);
//     chatDisplay.scrollTop = chatDisplay.scrollHeight;  // Scroll to the bottom
// }

// // Listen for the Enter key press on the input field
// document.getElementById('user-input').addEventListener('keydown', function(event) {
//     if (event.key === "Enter") {
//         event.preventDefault();
//         sendMessage();
//     }
// });

// // table
// document.addEventListener('DOMContentLoaded', function() {
//     // 在页面加载时获取飲食记录数据
//     fetch('/getdata')
//         .then(response => response.json())
//         .then(data => {
//             var table = document.getElementById('foodLog');
//             data.forEach(record => {
//                 var newRow = table.insertRow();
//                 var cell1 = newRow.insertCell(0);
//                 var cell2 = newRow.insertCell(1);
//                 var cell3 = newRow.insertCell(2);
//                 var cell4 = newRow.insertCell(3);
//                 var cell5 = newRow.insertCell(4);
//                 var cell6 = newRow.insertCell(5);
//                 cell1.innerHTML = record.Food;
//                 cell2.innerHTML = record.Cal;
//                 cell3.innerHTML = record.Carb;
//                 cell4.innerHTML = record.Protein;
//                 cell5.innerHTML = record.Fat;
//                 cell6.innerHTML = '<button onclick="deleteRow(this)">删除</button><button onclick="editRow(this)">修改</button>';
//             });
//         })
//         .catch(error => console.error('Error:', error));

//     // // 原有的添加新行的逻辑保持不变
//     // document.getElementById('addRow').addEventListener('click', function() {
//     //     var table = document.getElementById('foodLog');
//     //     var newRow = table.insertRow();
//     //     var cell1 = newRow.insertCell(0);
//     //     var cell2 = newRow.insertCell(1);
//     //     var cell3 = newRow.insertCell(2);
//     //     var cell4 = newRow.insertCell(3);
//     //     cell1.innerHTML = '日期输入';
//     //     cell2.innerHTML = '餐点输入';
//     //     cell3.innerHTML = '热量输入';
//     //     cell4.innerHTML = '<button onclick="deleteRow(this)">删除</button><button onclick="editRow(this)">修改</button>';
//     // });
// });

// // 删除和修改行的逻辑保持不变
// function deleteRow(btn) {
//     var row = btn.parentNode.parentNode;
//     row.parentNode.removeChild(row);
// }

// function editRow(btn) {
//     // 实现修改逻辑，可能需要添加表单元素以编辑内容
// }