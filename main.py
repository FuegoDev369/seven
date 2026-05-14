#!/usr/bin/env python3
"""
⚡ Seven — Ton agent IA personnel
Construit par FuegoDev (@ahry369)
"""

import argparse
import sys


BANNER = """
  ███████╗███████╗██╗   ██╗███████╗███╗   ██╗
  ██╔════╝██╔════╝██║   ██║██╔════╝████╗  ██║
  ███████╗█████╗  ██║   ██║█████╗  ██╔██╗ ██║
  ╚════██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
  ███████║███████╗ ╚████╔╝ ███████╗██║ ╚████║
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
  Agent IA personnel — by FuegoDev (@ahry369)
"""


def main():
    parser = argparse.ArgumentParser(
        prog='seven',
        description='⚡ Seven — Ton agent IA personnel pour Twitter/X',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commandes rapides :
  python main.py ideas                              → 5 idées de tweets
  python main.py ideas --topic "Python" -n 3       → Idées sur un sujet
  python main.py ideas --thread                    → Idées de threads

  python main.py write --idea "Tips Git"           → Tweet classique (3 versions)
  python main.py write --thread --idea "AI"        → Thread 8 tweets
  python main.py write --grand-ecart --idea "Git"  → Hook + Analogie + Exécution
  python main.py write --bilingual --idea "Web3"   → Tweet EN + Reply FR
  python main.py write --reformat "tweet..."       → Améliorer un tweet

  python main.py bip                               → Build in Public (interactif)
  python main.py bip --situation "mon bug"         → Galère → post authentique
  python main.py bip --situation "..." --type win  → Victoire → post humble

  python main.py sources                           → Toutes les sources
  python main.py sources --source github           → GitHub Trending seulement
  python main.py sources --source defi             → DeFiLlama seulement

  python main.py plan --week                       → Planning 7 jours
  python main.py plan --show                       → Voir le planning
  python main.py analyze "Mon tweet ici"           → Analyser un tweet
  python main.py trends                            → Tendances (DuckDuckGo + IA)
  python main.py notify --test                     → Tester les notifs
  python main.py daily                             → Run complet (GitHub Actions)
        """
    )

    sub = parser.add_subparsers(dest='command')

    # ideas
    p = sub.add_parser('ideas', help='Générer des idées de tweets/threads')
    p.add_argument('--topic', '-t', type=str)
    p.add_argument('--count', '-n', type=int, default=5)
    p.add_argument('--thread', action='store_true')

    # write
    p = sub.add_parser('write', help='Rédiger ou reformater un tweet')
    p.add_argument('--idea', '-i', type=str)
    p.add_argument('--reformat', '-r', type=str)
    p.add_argument('--thread', action='store_true')
    p.add_argument('--grand-ecart', action='store_true', help='Hook + Analogie + Exécution')
    p.add_argument('--bilingual', action='store_true', help='Tweet EN + Reply FR')

    # bip
    p = sub.add_parser('bip', help='Build in Public — galères, wins, learnings, progress')
    p.add_argument('--situation', '-s', type=str)
    p.add_argument('--type', '-t',
                   choices=['struggle', 'win', 'learning', 'progress'],
                   default=None)

    # sources
    p = sub.add_parser('sources', help='Hacker News · GitHub · DeFiLlama · Reddit')
    p.add_argument('--source', '-s', type=str, default=None,
                   help='hn | github | defi | reddit')

    # plan
    p = sub.add_parser('plan', help='Calendrier de contenu')
    p.add_argument('--show',  action='store_true')
    p.add_argument('--week',  action='store_true')
    p.add_argument('--add',   type=str)
    p.add_argument('--date',  type=str)

    # analyze
    p = sub.add_parser('analyze', help='Analyser un tweet')
    p.add_argument('tweet', type=str, nargs='?')
    p.add_argument('--file', '-f', type=str)

    # trends
    p = sub.add_parser('trends', help='Veille tendances')
    p.add_argument('--topic', '-t', type=str)

    # notify
    p = sub.add_parser('notify', help='Notifications Telegram/Discord')
    p.add_argument('--test',  action='store_true')
    p.add_argument('--daily', action='store_true')

    # daily (GitHub Actions)
    sub.add_parser('daily', help='Pipeline quotidien automatisé')

    args = parser.parse_args()

    if not args.command:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    try:
        from core.config import Config
        config = Config()
    except ValueError as e:
        print(f"\n❌ {e}")
        print("👉 Copie .env.example en .env et remplis tes clés API\n")
        sys.exit(1)

    if args.command == 'ideas':
        from modules.ideas import IdeasModule
        IdeasModule(config).run(topic=args.topic, count=args.count, thread=args.thread)

    elif args.command == 'write':
        from modules.writer import WriterModule
        WriterModule(config).run(
            idea        = args.idea,
            reformat    = args.reformat,
            thread      = args.thread,
            grand_ecart = getattr(args, 'grand_ecart', False),
            bilingual   = args.bilingual,
        )

    elif args.command == 'bip':
        from modules.bip import BipModule
        BipModule(config).run(
            situation = args.situation,
            bip_type  = args.type,
        )

    elif args.command == 'sources':
        from modules.sources import SourcesModule
        SourcesModule(config).run(source_filter=args.source)

    elif args.command == 'plan':
        from modules.planner import PlannerModule
        m = PlannerModule(config)
        if args.week:   m.generate_week()
        elif args.add:  m.add(args.add, args.date)
        else:           m.show()

    elif args.command == 'analyze':
        from modules.analyzer import AnalyzerModule
        AnalyzerModule(config).run(tweet=args.tweet, file=args.file)

    elif args.command == 'trends':
        from modules.trends import TrendsModule
        TrendsModule(config).run(topic=args.topic)

    elif args.command == 'notify':
        _notify(config, args)

    elif args.command == 'daily':
        _daily(config)


def _notify(config, args):
    notifiers = _get_notifiers(config)
    if not notifiers:
        print("⚠️  Aucun notifier configuré (Telegram ou Discord)")
        return
    if args.test:
        for n in notifiers:
            n.send("⚡ *Seven* — Test de notification ✅\nTout fonctionne !")
    elif args.daily:
        from modules.trends import TrendsModule
        msg = TrendsModule(config).get_briefing()
        for n in notifiers:
            n.send(msg)


def _daily(config):
    print("⚡ Seven — Daily Run\n" + "─" * 50)
    from modules.trends  import TrendsModule
    from modules.ideas   import IdeasModule
    from modules.sources import SourcesModule

    # 1. Sources brutes
    print("📡 Agrégation des sources (HN · GitHub · DeFiLlama · Reddit)...")
    src   = SourcesModule(config)
    data  = src.fetch_all()
    raw   = src._format_raw(data)

    # 2. Tendances IA
    print("🔍 Analyse des tendances...")
    trends_text = TrendsModule(config).get_trending_topics()

    # 3. Idées basées sur les deux
    print("💡 Génération d'idées...")
    context    = f"{trends_text}\n\n{raw[:600]}"
    ideas_text = IdeasModule(config).generate(count=5, context=context)

    # 4. Suggestions sources IA
    print("🤖 Analyse IA des sources...")
    suggestions = src.analyze_and_suggest(raw)

    message = (
        "⚡ *Seven — Daily Briefing*\n\n"
        "📈 *Tendances du moment*\n"
        f"{trends_text}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔥 *Opportunités (Sources)*\n"
        f"{suggestions}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 *Idées de contenu*\n"
        f"{ideas_text}\n\n"
        "_by Seven · FuegoDev 🔥_"
    )

    notifiers = _get_notifiers(config)
    if notifiers:
        for n in notifiers:
            n.send(message)
        print("✅ Briefing envoyé !")
    else:
        print("\n" + message)


def _get_notifiers(config):
    out = []
    if config.telegram_token and config.telegram_chat_id:
        from notifiers.telegram import TelegramNotifier
        out.append(TelegramNotifier(config))
    if config.discord_webhook:
        from notifiers.discord import DiscordNotifier
        out.append(DiscordNotifier(config))
    return out


if __name__ == '__main__':
    main()
