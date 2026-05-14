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

    def write_grand_ecart(self, idea: str) -> str:
        """Structure FuegoDev : Hook universel → Vulgarisation → Exécution technique."""
        return self.ai.ask(f"""Rédige un post Twitter/X pour FuegoDev en suivant la structure "Grand Écart" sur :
"{idea}"

La structure "Grand Écart" est la signature de FuegoDev :
elle s'adresse aux techs ET aux non-techs dans le même post.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERSION TWEET SIMPLE (max 280 chars)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Un seul tweet condensé en 3 niveaux : hook · analogie · commande/lien]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERSION THREAD (3 tweets)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1/ 🎯 HOOK — [Bénéfice immédiat ou problème résolu. S'adresse à TOUT le monde.]
   ex: "Pas besoin d'un PC à 2000€ pour lancer un serveur Python."

2/ 💡 VULGARISATION — [Analogie simple de la vie réelle. Explique le POURQUOI.]
   ex: "Votre téléphone est comme une usine endormie. Il lui faut juste le bon manuel."

3/ ⚡ EXÉCUTION — [Valeur technique concrète. Commande précise / prompt / lien GitHub.]
   ex: `pkg install python && python -m http.server`
   + hashtags ici seulement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 RECOMMANDATION : [quelle version poster + heure suggérée]

Règles absolues :
- Ligne 1 = tout le monde peut comprendre (pas de jargon)
- L'analogie doit être tirée de la vie quotidienne
- La partie technique doit être COPIER-COLLER directement""", max_tokens=2000)

    def write_bilingual(self, idea: str) -> str:
        """Tweet EN (portée globale) + Reply FR (proximité communauté francophone)."""
        return self.ai.ask(f"""Rédige un post Twitter/X bilingue pour FuegoDev sur :
"{idea}"

Stratégie bilingue de FuegoDev :
• Corps du tweet en ANGLAIS → portée globale, algorithme mondial
• Reply/thread en FRANÇAIS → proximité avec la communauté francophone

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 TWEET PRINCIPAL (EN) — max 280 chars
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Tweet en anglais — hook fort · valeur claire · 2-3 hashtags EN]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇫🇷 REPLY FRANÇAIS (à poster en réponse)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Traduction naturelle + context FR + éventuellement plus de détails]
[Pas une traduction mot à mot — adapte le ton pour la communauté FR]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧵 VERSION THREAD BILINGUE (bonus)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1/ [Hook EN]
2/ [Développement EN]
3/ [🇫🇷 Pour la communauté française : version FR du contenu]
4/ [CTA bilingue + hashtags]

Règles : l'anglais doit sonner naturel (pas de traducteur) · le français doit avoir une touche personnelle FuegoDev""", max_tokens=2000)

    def run(self, idea=None, reformat=None, thread=False,
            grand_ecart=False, bilingual=False):
        print(f"\n⚡ Seven — Rédaction\n{'─'*52}")

        if reformat:
            print("✏️  Reformatage…\n")
            print(self.reformat(reformat))

        elif grand_ecart and idea:
            print(f"🎯 Grand Écart : {idea}\n")
            print(self.write_grand_ecart(idea))

        elif bilingual and idea:
            print(f"🌍 Bilingue EN+FR : {idea}\n")
            print(self.write_bilingual(idea))

        elif idea and thread:
            print(f"🧵 Thread : {idea}\n")
            print(self.write_thread(idea))

        elif idea:
            print(f"📝 Tweet : {idea}\n")
            print(self.write_tweet(idea))

        else:
            try:
                idea = input("💡 Sujet : ").strip()
                print("\nFormat ?")
                print("  1 → Tweet classique (3 versions)")
                print("  2 → Thread (8 tweets)")
                print("  3 → Grand Écart (Hook + Analogie + Exécution)")
                print("  4 → Bilingue (EN tweet + FR reply)")
                choice = input("Choix (1-4) : ").strip()
                print()
                dispatch = {
                    "2": self.write_thread,
                    "3": self.write_grand_ecart,
                    "4": self.write_bilingual,
                }
                print(dispatch.get(choice, self.write_tweet)(idea))
            except (EOFError, KeyboardInterrupt):
                print("⚠️  Utilise --idea ou --reformat")
