import requests


class TelegramNotifier:
    def __init__(self, config):
        self.token   = config.telegram_token
        self.chat_id = config.telegram_chat_id
        self.url     = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str) -> bool:
        for chunk in [message[i:i+4000] for i in range(0, len(message), 4000)]:
            r = requests.post(self.url, json={
                "chat_id": self.chat_id, "text": chunk, "parse_mode": "Markdown"
            }, timeout=10)
            ok = r.status_code == 200
            print("✅ Telegram envoyé !" if ok else f"❌ Telegram erreur : {r.text}")
        return ok
