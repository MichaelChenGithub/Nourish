# app.py

from flask import Flask, render_template, request
from chat_logic.chat_logic_main import execute_chat

app = Flask(__name__)

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    response = execute_chat(user_message, chat_history)
    return response

if __name__ == '__main__':
    app.run(debug=True)
