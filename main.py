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
  python main.py ideas                         → 5 idées de tweets
  python main.py ideas --topic "Python" -n 3  → Idées sur un sujet
  python main.py ideas --thread               → Idées de threads
  python main.py write --idea "Tips Git"      → Rédiger un tweet
  python main.py write --thread --idea "AI"   → Rédiger un thread
  python main.py write --reformat "tweet..."  → Améliorer un tweet
  python main.py plan --week                  → Planning 7 jours
  python main.py plan --show                  → Voir le planning
  python main.py analyze "Mon tweet ici"      → Analyser un tweet
  python main.py trends                       → Tendances actuelles
  python main.py notify --test                → Tester les notifs
  python main.py daily                        → Run complet (CI/CD)
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
        WriterModule(config).run(idea=args.idea, reformat=args.reformat, thread=args.thread)

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
    from modules.trends import TrendsModule
    from modules.ideas  import IdeasModule

    print("📡 Veille tendances...")
    trends_text = TrendsModule(config).get_trending_topics()

    print("💡 Génération d'idées...")
    ideas_text = IdeasModule(config).generate(count=5, context=trends_text)

    message = (
        "⚡ *Seven — Daily Briefing*\n\n"
        "📈 *Tendances du moment*\n"
        f"{trends_text}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 *Idées de contenu aujourd'hui*\n"
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
