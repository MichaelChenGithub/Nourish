// 設置cookie的函數
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

$(document).ready(function() {
    function checkTokenAndRedirect() {
        var token = getTokenFromCookie(); // 假设令牌存储在cookie中
        console.log(token)
        if (token) {
            window.location.href = '/chat'; // 如果令牌不存在，则重定向到登录页面
        }
    }

    checkTokenAndRedirect();
});


$(document).ready(
    function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // 防止表單自動提交

        var username = $('#username').val();
        var password = $('#password').val();

        // 發送 POST 請求到後端登入端點
        $.ajax({
            url: '/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username: username, password: password }),
            success: function(response) {
                // 登入成功，後端將會進行頁面跳轉，不需要在前端進行任何跳轉操作
                console.log('Login success!');
                // 登入成功後將 token 存儲在 cookie 中
                setCookie('token', response, 30); // 這裡的30表示token的過期時間為30天
                // 跳轉到聊天頁面並帶有 token
                window.location.href = '/chat';
            },
            error: function(xhr, status, error) {
                // 登入失敗，顯示錯誤信息
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.message : 'An error occurred';
                alert(errorMessage);
            }
        });
    });
});

