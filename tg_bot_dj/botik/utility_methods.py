import requests
from decouple import config

TELEGRAM_API_URL = f'https://api.telegram.org/bot{config("BOTIK_TOKEN")}/'
send_prefix = "sendMessage"
delete_prefix = "deleteMessage"

#DELETE_URL = f'https://api.telegram.org/bot{config('BOTIK_TOKEN')}/deleteMessage'

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(TELEGRAM_API_URL+send_prefix, json=payload)
    if response.ok:
        data = response.json()
        return data['result']['message_id']
    return None