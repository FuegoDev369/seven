from core.ai import AIClient
from core.database import Database


class IdeasModule:
    def __init__(self, config):
        self.ai     = AIClient(config)
        self.db     = Database(config.db_path)
        self.config = config

    def generate(self, count=5, topic=None, thread=False, context="") -> str:
        fmt      = "thread Twitter (série de tweets numérotés)" if thread else "tweet"
        topic_st = f"sur : **{topic}**" if topic \
                   else f"sur tes sujets : {', '.join(self.config.content_topics)}"
        ctx      = f"\n🌐 Contexte tendances :\n{context[:800]}\n" if context else ""

        prompt = f"""Génère {count} idées originales de {fmt} {topic_st}.
{ctx}
Format pour chaque idée :

━━━━━━━━━━━━━━━━━━━━━━━━
💡 IDÉE [N] — [titre accrocheur]
🔥 HOOK     : [première ligne irrésistible]
📌 CONCEPT  : [ce que le lecteur va apprendre, en 1-2 phrases]
🎯 ANGLE    : [ce qui le rend unique]
#️⃣  HASHTAGS : [2-3 hashtags]
━━━━━━━━━━━━━━━━━━━━━━━━

Critères : éducatif ✅ actuel ✅ authentique FuegoDev ✅ varié ✅"""

        return self.ai.ask(prompt)

    def run(self, topic=None, count=5, thread=False):
        fmt = "threads" if thread else "tweets"
        print(f"\n⚡ Seven — Idées de {fmt}\n{'─'*52}")
        if topic:
            print(f"📌 Sujet : {topic}\n")

        result = self.generate(count=count, topic=topic, thread=thread)
        print(result)

        try:
            if input("\n💾 Sauvegarder ? (o/n) : ").strip().lower() == 'o':
                self.db.save_idea(result, topic or 'mixed')
                print("✅ Sauvegardé !")
        except (EOFError, KeyboardInterrupt):
            pass
