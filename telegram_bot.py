import os

from dotenv import load_dotenv
from requests import Session

load_dotenv(dotenv_path='.env')


class TelegramBot:
    def __init__(self):
        self.session = Session()
        self.telegram_token = os.environ['TELEGRAM_TOKEN']
        self.chat_id = os.environ['USER_CHAT_ID']

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }
        self.session.request("POST", url, data=payload)
