"""
⚡ Seven — Build in Public (BIP)
Transforme tes galères de code, progrès et apprentissages
en posts authentiques qui créent de l'attachement.
"""

from core.ai import AIClient


class BipModule:
    def __init__(self, config):
        self.ai     = AIClient(config)
        self.config = config

    # ── Générateurs ──────────────────────────────────────────────────────────

    def from_struggle(self, situation: str) -> str:
        """Bug, erreur, galère → post authentique."""
        return self.ai.ask(f"""FuegoDev a vécu cette situation de code :
"{situation}"

Transforme ça en post Build in Public authentique.

VERSION 1 — Tweet simple (max 280 chars)
[Post honnête sur la galère + ce qu'il a appris]
#️⃣ [hashtags]

VERSION 2 — Thread court (3 tweets)
1/ [La galère en mode honnête — le hook]
2/ [Ce qui s'est passé exactement + ce que ça a appris]
3/ [La solution + conseil pour éviter ça + CTA]

VERSION 3 — Storytelling (angle "behind the scenes")
[Raconte l'histoire de façon engageante, humaine, drôle si possible]

RECOMMANDATION : [laquelle poster et pourquoi]

Règles : authentique avant tout · pas de "j'ai réussi" fake · le doute et l'honnêteté créent plus d'engagement que la perfection""")

    def from_win(self, situation: str) -> str:
        """Victoire, réussite, milestone → post motivant sans paraître arrogant."""
        return self.ai.ask(f"""FuegoDev a accompli quelque chose :
"{situation}"

Transforme ça en post Build in Public qui célèbre sans être arrogant.

VERSION 1 — Tweet simple
[Célébration humble + ce qui a rendu ça possible]

VERSION 2 — Thread de gratitude + valeur
1/ [L'annonce du win — hook fort mais humble]
2/ [Le parcours — les difficultés traversées]
3/ [Ce que ça lui a appris + conseil actionnable]
4/ [Remerciements + CTA]

VERSION 3 — Angle "process" (ce qui a vraiment marché)
[Focus sur la méthode plutôt que le résultat]

RECOMMANDATION : [laquelle poster et pourquoi]""")

    def from_learning(self, situation: str) -> str:
        """Ce que tu as appris aujourd'hui → post éducatif personnel."""
        return self.ai.ask(f"""FuegoDev vient d'apprendre ou de découvrir :
"{situation}"

Transforme ça en post "Today I Learned" engageant.

VERSION 1 — TIL Tweet
[TIL court et percutant — max 280 chars]

VERSION 2 — Thread "Grand Écart" (structure FuegoDev)
1/ HOOK    : [Accroche universelle — accessible à tous]
2/ CONCEPT : [Analogie simple — le "pourquoi"]
3/ TECH    : [La valeur concrète — commande, prompt ou lien]
4/ CTA     : [Question ou invitation à partager]

VERSION 3 — Question pour engager la communauté
[Transforme l'apprentissage en question ouverte pour le réseau]

RECOMMANDATION : [laquelle poster et pourquoi]""")

    def from_progress(self, situation: str) -> str:
        """Mise à jour de progression sur un projet (ex: LUDUS, Seven...)."""
        return self.ai.ask(f"""FuegoDev partage une mise à jour sur son projet :
"{situation}"

Génère un post de progression Build in Public.

VERSION 1 — Update tweet
[État d'avancement honnête en moins de 280 chars]

VERSION 2 — Thread "progress log"
1/ [Ce qui était prévu]
2/ [Ce qui a été fait réellement]
3/ [Ce qui a bloqué]
4/ [Prochain milestone + ce qu'on peut apprendre de ça]

VERSION 3 — Angle "making of"
[Montre les coulisses du projet de façon engageante]

RECOMMANDATION : [laquelle et pourquoi]

⚠️ Important : jamais de fausse modestie, jamais d'exagération — juste la vérité du processus.""")

    # ── Entry point CLI ──────────────────────────────────────────────────────

    def run(self, situation: str = None, bip_type: str = None):
        print(f"\n⚡ Seven — Build in Public\n{'─'*52}")

        if not situation:
            try:
                print("Raconte-moi ce qui s'est passé aujourd'hui dans ton projet.\n")
                situation = input("📝 Ta situation : ").strip()
                if not situation:
                    print("⚠️  Fournis une situation avec --situation")
                    return
            except (EOFError, KeyboardInterrupt):
                print("⚠️  Usage : python main.py bip --situation \"mon bug d'aujourd'hui\"")
                return

        if not bip_type:
            try:
                print("\nQuel type de moment ?")
                print("  1 → Galère / Bug / Erreur")
                print("  2 → Victoire / Réussite")
                print("  3 → Apprentissage / Découverte")
                print("  4 → Mise à jour projet")
                choice = input("\nChoix (1-4) : ").strip()
                bip_type = {"1": "struggle", "2": "win",
                             "3": "learning", "4": "progress"}.get(choice, "struggle")
            except (EOFError, KeyboardInterrupt):
                bip_type = "struggle"

        print(f"\n🤖 Génération du post BIP ({bip_type})…\n")

        generators = {
            "struggle": self.from_struggle,
            "win":      self.from_win,
            "learning": self.from_learning,
            "progress": self.from_progress,
        }
        result = generators.get(bip_type, self.from_struggle)(situation)
        print(result)
