from core.ai import AIClient
from core.search import search_multi


class TrendsModule:
    def __init__(self, config):
        self.ai     = AIClient(config)
        self.config = config

    def get_trending_topics(self, topic: str = None) -> str:
        subjects = topic or ', '.join(self.config.content_topics)

        # 1. Recherche DuckDuckGo (gratuit, pas de clé)
        queries = [f"{s} trends 2025 2026" for s in subjects.split(',')[:3]]
        print(f"   🔍 Recherche web : {', '.join(queries[:2])}…")
        web_context = search_multi(queries, max_per_query=4)

        # 2. Analyse IA avec le contexte web
        prompt = f"""Sur la base des résultats de recherche ci-dessus, analyse les tendances actuelles pour : {subjects}.

Pour chaque domaine pertinent, identifie :

🔥 [DOMAINE]
├── Tendance #1 : [sujet précis] — [pourquoi c'est chaud]
├── Tendance #2 : [sujet précis] — [pourquoi c'est chaud]
└── Tendance #3 : [sujet précis] — [pourquoi c'est chaud]

Puis, pour FuegoDev (@ahry369) :

💡 OPPORTUNITÉS DE CONTENU
┌──────────────────────────────────────
│ 🚀 À poster MAINTENANT
│    → [sujet + angle FuegoDev]
│
│ 📅 Cette semaine
│    → [sujet + angle FuegoDev]
│
│ 🔮 À surveiller
│    → [sujet + angle FuegoDev]
└──────────────────────────────────────

Sois précis, cite des outils/projets/événements réels issus des résultats."""

        return self.ai.ask_with_context(prompt, web_context)

    def get_briefing(self) -> str:
        trends = self.get_trending_topics()
        return (
            "⚡ *Seven — Daily Briefing*\n\n"
            "📈 *Tendances du moment*\n"
            f"{trends}\n\n"
            "_by Seven · FuegoDev 🔥_"
        )

    def run(self, topic: str = None):
        print(f"\n⚡ Seven — Veille tendances\n{'─'*52}")
        print("🌐 Recherche web en cours (DuckDuckGo)…\n")
        result = self.get_trending_topics(topic)
        print(result)
