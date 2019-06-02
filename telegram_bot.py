from requests import Session
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class TelegramBot:
    def __init__(self):
        self.session = Session()
        self.telegram_token = os.environ['TELEGRAM_TOKEN']
        self.chat_id = os.environ['CHAT_ID']

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        self.session.request("POST", url, data=payload)
