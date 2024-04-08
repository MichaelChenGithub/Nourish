# app.py

from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
from chat_logic.chat_logic_main import execute_chat
from functools import wraps
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = "9Y4QNeZz47U8KucJ3jW2gDvHxyPBmrFp"

# 假設這是你的用戶資料庫
users = {
    "abc": "123"
}
# 假設這是要发送到前端的飲食記錄數據
records_data = [
    {'Food': "Cheese Burger", 'Cal': 400, 'Carb': 300, "Protein": 100, "Fat": 20},
    {'Food': "Cheese Burger", 'Cal': 400, 'Carb': 300, "Protein": 100, "Fat": 20},
]
diet_objective = "My goal is to lose 4 kilograms within the next two months using the 16/8 intermittent fasting method."

chat_history = []


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # 假设你使用 JWT 进行身份验证
            token = token.split(' ')[1]  # 去掉 Bearer 前缀
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth = request.get_json()

        if not auth or not auth['username'] or not auth['password']:
            return jsonify({'message': 'Could not verify!'}), 401

        if auth['username'] in users and users[auth['username']] == auth['password']:
            token = jwt.encode({'username': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            # 回傳 token
            return token

        return jsonify({'message': 'Could not verify!'}), 401
    else:
        return render_template('login.html')

@app.route('/chat', methods=['GET'])
def show_chat_page(*args, **kwargs):
    # 在這裡處理 GET 請求，不需要驗證用戶身份
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
# @token_required
def handle_chat_message(*args, **kwargs):
    current_user = kwargs.get('current_user')  # 从kwargs中获取current_user
    user_message = request.form['user_message']
    if user_message == "What should I eat now?":
        user_message = diet_objective + str(records_data) + "What should I eat now?"
        print(user_message)
    response = execute_chat(user_message, chat_history)
    return response

@app.route('/records')
# @token_required
def records():
    return render_template('records.html', records=records_data, diet_objective=diet_objective)

if __name__ == '__main__':
    app.run(debug=True)
