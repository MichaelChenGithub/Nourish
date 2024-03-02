# app.py

from flask import Flask, render_template, request
from chat_logic.chat_logic_main import execute_chat


app = Flask(__name__)

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/records')
# def home():
#     return render_template('records.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    response = execute_chat(user_message, chat_history)
    return response

import pandas as pd
# 假设这是你的飲食紀錄 DataFrame
data = {
    '日期': ['2024-03-01', '2024-03-02', '2024-03-03'],
    '食物': ['燕麥片', '三明治', '雞胸肉'],
    '飲料': ['水、茶', '茶、咖啡', '水'],
    '備註': ['無', '無', '無']
}
df = pd.DataFrame(data)

@app.route('/records')
def records():
    # 将 DataFrame 转换为 HTML 字符串
    records_html = df.to_html(index=False)
    return render_template('records.html', records_html=records_html)

if __name__ == '__main__':
    app.run(debug=True)
