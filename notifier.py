# notifier.py
import os, requests
TELE_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELE_CHAT = os.environ.get('TELEGRAM_CHAT_ID')

def send_msg(text):
    if not TELE_TOKEN or not TELE_CHAT:
        print('Telegram not configured. Message would be:\n', text)
        return
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELE_CHAT, "text": text, "parse_mode":"HTML"})

if __name__ == '__main__':
    send_msg('Agent test message: hello from job agent.')
