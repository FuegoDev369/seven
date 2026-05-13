import re
from core.ai import AIClient
from core.database import Database


class AnalyzerModule:
    def __init__(self, config):
        self.ai = AIClient(config)
        self.db = Database(config.db_path)

    def analyze(self, tweet: str) -> str:
        return self.ai.ask(f"""Analyse ce tweet de FuegoDev :
"{tweet}"

📊 SCORE GLOBAL : [X/10]

🎯 Hook          : [X/10] — [commentaire]
📖 Clarté        : [X/10] — [commentaire]
💎 Valeur        : [X/10] — [commentaire]
🔥 Engagement    : [X/10] — [commentaire]
🏷️  Hashtags      : [ok ✅ / manquants ⚠️ / en trop ❌]
📏 Longueur      : [X/280 chars]
🎨 Authenticité  : [style FuegoDev ? oui/non]

⚡ POINTS FORTS
• ...

🔧 AMÉLIORATIONS
• ...

✏️ VERSION OPTIMISÉE
[Tweet réécrit — max 280 chars]""")

    def _score(self, text: str) -> int:
        m = re.search(r'SCORE GLOBAL\s*:\s*\[?(\d+)', text)
        return int(m.group(1)) if m else 0

    def run(self, tweet=None, file=None):
        print(f"\n⚡ Seven — Analyse\n{'─'*52}")

        if file:
            try:
                tweets = [l.strip() for l in open(file, encoding='utf-8') if l.strip()]
                for i, t in enumerate(tweets, 1):
                    print(f"\n{'═'*52}\n📝 Tweet {i}/{len(tweets)}\n{'═'*52}")
                    r = self.analyze(t)
                    print(r)
                    self.db.save_analysis(t, r, self._score(r))
            except FileNotFoundError:
                print(f"❌ Fichier introuvable : {file}")
            return

        if not tweet:
            try:
                tweet = input("📝 Tweet à analyser : ").strip()
            except (EOFError, KeyboardInterrupt):
                print('⚠️  Usage : python main.py analyze "ton tweet"')
                return

        r = self.analyze(tweet)
        print(r)
        score = self._score(r)
        self.db.save_analysis(tweet, r, score)
        print(f"\n💾 Analyse sauvegardée (score : {score}/10)")
