from flask import Flask, request
from chat_logic.chat_logic_main import execute_chat
import json
from linebot.v3 import WebhookHandler
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os
from dotenv import load_dotenv

class LineBotApp:
    def __init__(self):
        self.app = Flask(__name__)
        load_dotenv()
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.secret = os.getenv('SECRET')

        self.line_bot_api = LineBotApi(self.access_token)
        self.handler = WebhookHandler(self.secret)
        self.setup_routes()
        
        self.user_chat_histories = {}

    def load_line_api_keys(self, filepath):
        keys = {}
        with open(filepath, 'r') as file:
            for line in file:
                key, value = line.strip().split(':', 1)
                keys[key.strip()] = value.strip()
        return keys

    def setup_routes(self):
        @self.app.route("/", methods=['POST'])
        def linebot():
            body = request.get_data(as_text=True)
            try:
                json_data = json.loads(body)
                signature = request.headers['X-Line-Signature']
                self.handler.handle(body, signature)
                tk = json_data['events'][0]['replyToken']
                msg_type = json_data['events'][0]['message']['type']
                
                user_id = json_data['events'][0]['source']['userId']
                if user_id not in self.user_chat_histories:
                    self.user_chat_histories[user_id] = []  # 為新用戶初始化聊天歷史
                
                chat_history = self.user_chat_histories[user_id]
                
                if msg_type == 'text':
                    
                    msg = str(json_data['events'][0]['message']['text'])
                    print(f'User:{msg}')
                    chat_history.append({"role": "user", "content": msg})
                    
                    reply = str(execute_chat(msg,chat_history))
                    print(f"reply:{reply}")
                    chat_history.append({"role": "assistant", "content": reply})
                    print(chat_history)
                else:
                    reply = '你傳的不是文字呦～'
                print(f'Reply:{reply}')
                self.line_bot_api.reply_message(tk, TextSendMessage(reply))
            except Exception as e:
                print(e)
                print(body)
            return 'OK'

if __name__ == "__main__":
    line_bot_app = LineBotApp()
    line_bot_app.app.run()