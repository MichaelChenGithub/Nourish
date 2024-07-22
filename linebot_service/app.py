from flask import Flask, request
from chat_logic.chat_logic_main import execute_chat
import json
import requests
from linebot.v3 import WebhookHandler
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioSendMessage
import os
import logging
from dotenv import load_dotenv


app = Flask(__name__)

class LineBotApp:
    def __init__(self):
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.secret = os.getenv('SECRET')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.subdomain = os.getenv('SUBDOMAIN')

        self.line_bot_api = LineBotApi(self.access_token)
        self.handler = WebhookHandler(self.secret)
        self.user_chat_histories = {}

    def display_loading_animation(self, chat_id, loading_seconds=10):
        url = "https://api.line.me/v2/bot/chat/loading/start"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        payload = {
            "chatId": chat_id,
            "loadingSeconds": loading_seconds
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                logging.info("Loading animation started successfully")
            else:
                logging.error(f"Failed to start loading animation: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logging.error(f"Exception during loading animation request: {e}")

    def generate_questions(self):
        questions_list = ["料理詳細步驟", "食譜的營養成分"]
        return questions_list
       
    def linebot(self):
        body = request.get_data(as_text=True)
        try:
            json_data = json.loads(body)
            signature = request.headers['X-Line-Signature']
            self.handler.handle(body, signature)
            tk = json_data['events'][0]['replyToken']
            msg_type = json_data['events'][0]['message']['type']
            source_type = json_data['events'][0]['source']['type']
            user_id = json_data['events'][0]['source']['userId']

            logging.info(f"Request body: {body}")
            # 顯示載入動畫
            self.display_loading_animation(user_id)
            # user_information = self.record_manager.get_or_create_user_usage(user_id)
            
            ############### text ################
            if msg_type == 'text':
                msg = str(json_data['events'][0]['message']['text']) 
                reply = str(execute_chat(msg, []))
                # self.record_manager.add_chat_record(user_id, "user", msg, user_information)
                # reply = str(self.chat.execute_chat(msg, user_information['chat_history']))
                # self.record_manager.add_chat_record(user_id, "assistant", reply, user_information)
            ############### image ################
            # elif msg_type == 'image':
                # if user_information['model_version'] == 4 and user_information['GTP 4o frequency of use'] < GPT_4o_Limit:
                #     # 根據訊息 ID 取得訊息內容
                #     message_content = self.line_bot_api.get_message_content(json_data['events'][0]['message']['id'])  
                #     # 設定要儲存圖片的資料夾路徑
                #     folder_path = 'image_buffer'
                #     os.makedirs(folder_path, exist_ok=True)
                    
                #     # 在指定的資料夾中建立以 user_id 為檔名的 .jpg 檔案
                #     file_path = os.path.join(folder_path, f'{user_id}.jpg')
                #     with open(file_path, 'wb') as fd:
                #         fd.write(message_content.content)

                #     reply = self.image_description.get_image_description(file_path)
                #     self.record_manager.add_chat_record(user_id, "assistant", reply, user_information)
                # else:
                #     reply = "GPT4o模型才能做圖片辨識喔～"
            else:
                reply = "目前只支援文字訊息喔～"

            # Generate quick reply buttons
            questions = self.generate_questions(msg_type, source_type)
            quick_reply_items = [QuickReplyButton(action=MessageAction(label=question, text=question)) for question in questions]
            quick_reply = QuickReply(items=quick_reply_items)
            
            # Create a message with quick reply buttons
            reply_message = TextSendMessage(text=reply, quick_reply=quick_reply)

            self.line_bot_api.reply_message(tk, reply_message)
            logging.info(f'Reply: {reply}')
        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(f"Request body: {body}")
        return 'OK'

line_bot_app = LineBotApp()

@app.route("/", methods=['POST'])
def webhook():
    return line_bot_app.linebot()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)