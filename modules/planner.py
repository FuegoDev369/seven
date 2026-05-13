from datetime import datetime, timedelta
from core.ai import AIClient
from core.database import Database


class PlannerModule:
    def __init__(self, config):
        self.ai   = AIClient(config)
        self.db   = Database(config.db_path)
        self.cfg  = config

    def generate_week(self):
        today = datetime.now()
        dates = [(today + timedelta(days=i)).strftime('%A %d/%m') for i in range(7)]

        prompt = f"""Crée un planning Twitter 7 jours pour FuegoDev (@ahry369).

Jours : {', '.join(dates)}
Sujets : {', '.join(self.cfg.content_topics)}

Pour chaque jour :
📅 [Jour + date]
│ TYPE     : [Tweet / Thread / Question / Tip / Sondage]
│ SUJET    : [Thème précis]
│ OBJECTIF : [Informer / Engager / Inspirer]
│ HOOK     : [Première ligne]
│ HEURE    : [Créneau suggéré]
│ HASHTAGS : [2-3 hashtags]

Règles : alterner les formats · au moins 1 thread · 1 question · 1 tip pratique dans la semaine."""

        result = self.ai.ask(prompt, max_tokens=3000)
        print(f"\n⚡ Seven — Planning 7 jours\n{'─'*52}")
        print(result)

        try:
            if input("\n💾 Sauvegarder ? (o/n) : ").strip().lower() == 'o':
                self.db.add_to_plan(today.strftime('%Y-%m-%d'), result, 'weekly_plan')
                print("✅ Planning sauvegardé !")
        except (EOFError, KeyboardInterrupt):
            pass

    def show(self):
        rows = self.db.get_plan()
        print(f"\n⚡ Seven — Calendrier\n{'─'*52}")
        if not rows:
            print("📭 Aucun contenu planifié.\n👉 Lance : python main.py plan --week")
            return
        for date, content, ctype, status in rows:
            icon = "✅" if status == "posted" else "📅"
            print(f"\n{icon} {date}  [{ctype}]")
            print(f"   {content[:100].replace(chr(10), ' ')}…")

    def add(self, content, date=None):
        date = date or datetime.now().strftime('%Y-%m-%d')
        self.db.add_to_plan(date, content)
        print(f"✅ Ajouté pour le {date}")
