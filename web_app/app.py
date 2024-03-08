# app.py

from flask import Flask, render_template, request, jsonify
from chat_logic.chat_logic_main import execute_chat


app = Flask(__name__)

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    response = execute_chat(user_message, chat_history)
    return response

@app.route('/getdata')
def get_data():
    # 假设这是要发送到前端的飲食记录数据
    records = [
        {'Food': "摩斯熱狗堡", 'Cal': 400, 'Carb': 300, "Protein": 100,"Fat": 20},
        {'Food': "摩斯熱狗堡", 'Cal': 400, 'Carb': 300, "Protein": 100,"Fat": 20},
    ]
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
