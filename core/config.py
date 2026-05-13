import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        # ── Provider IA ──────────────────────────────────────
        # "groq" (défaut, gratuit) | "gemini" (gratuit) | "anthropic" (premium)
        self.ai_provider = os.getenv('AI_PROVIDER', 'groq').lower()

        self.groq_key      = os.getenv('GROQ_API_KEY', '')
        self.gemini_key    = os.getenv('GEMINI_API_KEY', '')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')

        # ── Notifications ────────────────────────────────────
        self.telegram_token   = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        self.discord_webhook  = os.getenv('DISCORD_WEBHOOK_URL', '')

        # ── Identité ─────────────────────────────────────────
        self.twitter_username = os.getenv('TWITTER_USERNAME', '@ahry369')
        self.author_name      = os.getenv('AUTHOR_NAME', 'FuegoDev')

        # ── Contenu ──────────────────────────────────────────
        self.content_topics = [
            t.strip() for t in
            os.getenv('CONTENT_TOPICS', 'Dev,AI,Web3,Education,Tech').split(',')
        ]
        self.content_style = os.getenv(
            'CONTENT_STYLE', 'Éducatif, inspirant, pratique, authentique'
        )
        self.language = os.getenv('LANGUAGE', 'Français')

        # ── Stockage ─────────────────────────────────────────
        self.db_path = os.getenv('DB_PATH', 'seven.db')

        # ── Validation ───────────────────────────────────────
        self._validate()

    def _validate(self):
        required = {
            'groq':      (self.groq_key,      'GROQ_API_KEY'),
            'gemini':    (self.gemini_key,     'GEMINI_API_KEY'),
            'anthropic': (self.anthropic_key,  'ANTHROPIC_API_KEY'),
        }
        key, env_name = required.get(self.ai_provider, (None, None))
        if key is None:
            raise ValueError(
                f"Provider inconnu : '{self.ai_provider}'. "
                "Choisis : groq | gemini | anthropic"
            )
        if not key:
            raise ValueError(
                f"Clé API manquante pour le provider '{self.ai_provider}'.\n"
                f"   → Ajoute {env_name}=... dans ton fichier .env\n"
                f"   → Inscription gratuite : {self._signup_url()}"
            )

    def _signup_url(self):
        return {
            'groq':   'https://console.groq.com',
            'gemini': 'https://aistudio.google.com/app/apikey',
        }.get(self.ai_provider, 'https://console.anthropic.com')
