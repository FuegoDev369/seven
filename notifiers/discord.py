import requests


class DiscordNotifier:
    def __init__(self, config):
        self.url = config.discord_webhook

    def send(self, message: str) -> bool:
        ok = True
        for chunk in [message[i:i+1900] for i in range(0, len(message), 1900)]:
            r = requests.post(self.url, json={"content": chunk}, timeout=10)
            if r.status_code not in (200, 204):
                print(f"❌ Discord erreur : {r.text}")
                ok = False
            else:
                print("✅ Discord envoyé !")
        return ok
