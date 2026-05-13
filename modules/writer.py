from core.ai import AIClient


class WriterModule:
    def __init__(self, config):
        self.ai = AIClient(config)

    def write_tweet(self, idea: str) -> str:
        return self.ai.ask(f"""Rédige 3 versions d'un tweet pour FuegoDev basé sur :
"{idea}"

─────────────────────────────
📌 VERSION 1 — Tips / Éducatif
[Tweet max 280 caractères]
→ Pourquoi ça marche : [raison courte]

─────────────────────────────
📖 VERSION 2 — Storytelling
[Tweet max 280 caractères]
→ Pourquoi ça marche : [raison courte]

─────────────────────────────
💬 VERSION 3 — Question / Engagement
[Tweet max 280 caractères]
→ Pourquoi ça marche : [raison courte]

─────────────────────────────
🏆 RECOMMANDATION : Version X — [raison en 1 phrase]

Règles : hook fort en ligne 1 · max 280 chars · 2-3 hashtags · ton authentique FuegoDev""")

    def write_thread(self, idea: str) -> str:
        return self.ai.ask(f"""Rédige un thread de 8 tweets pour FuegoDev sur :
"{idea}"

🧵 1/8 — HOOK (accroche forte + promesse)
📌 2/8 — Contexte / problème
💡 3/8 à 7/8 — Un point clé concret par tweet
🎯 8/8 — Récap + CTA + hashtags (seulement sur ce dernier)

Règles : max 280 chars/tweet · numérotés · chaque tweet lisible seul · style FuegoDev""", max_tokens=3000)

    def reformat(self, tweet: str) -> str:
        return self.ai.ask(f"""Analyse et améliore ce tweet :
"{tweet}"

🔍 DIAGNOSTIC
• Hook / Clarté / Longueur / Hashtags / Engagement : [évaluation rapide]

✏️ VERSION AMÉLIORÉE
[Tweet optimisé — max 280 chars]

🔄 ALTERNATIVE
[Deuxième angle différent]

📋 CHANGEMENTS CLÉS : [liste courte]""")

    def run(self, idea=None, reformat=None, thread=False):
        print(f"\n⚡ Seven — Rédaction\n{'─'*52}")

        if reformat:
            print("✏️  Reformatage…\n")
            print(self.reformat(reformat))
        elif idea and thread:
            print(f"🧵 Thread : {idea}\n")
            print(self.write_thread(idea))
        elif idea:
            print(f"📝 Tweet : {idea}\n")
            print(self.write_tweet(idea))
        else:
            try:
                idea   = input("💡 Sujet : ").strip()
                choice = input("Format (1=tweet  2=thread) : ").strip()
                print()
                print(self.write_thread(idea) if choice == '2' else self.write_tweet(idea))
            except (EOFError, KeyboardInterrupt):
                print("⚠️  Utilise --idea ou --reformat")
