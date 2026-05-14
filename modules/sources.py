"""
⚡ Seven — Sources d'inspiration
Agrège les meilleurs contenus depuis :
  • Hacker News  (API officielle, gratuite)
  • GitHub Trending (scrape léger)
  • DeFiLlama     (API officielle, gratuite)
  • Reddit         (JSON public, sans clé)
Aucune clé API requise.
"""

import requests

HEADERS = {"User-Agent": "seven-agent/1.0 (FuegoDev @ahry369)"}
TIMEOUT = 8


# ── Hacker News ───────────────────────────────────────────────────────────────

def fetch_hackernews(limit: int = 5) -> list[dict]:
    """Top stories Hacker News."""
    try:
        ids = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=TIMEOUT
        ).json()[:limit * 2]

        stories = []
        for sid in ids[:limit * 2]:
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                timeout=TIMEOUT
            ).json()
            if item and item.get("type") == "story" and item.get("title"):
                stories.append({
                    "title": item.get("title", ""),
                    "url":   item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    "score": item.get("score", 0),
                })
            if len(stories) >= limit:
                break

        return stories
    except Exception as e:
        return [{"title": f"[Hacker News indisponible : {e}]", "url": "", "score": 0}]


# ── GitHub Trending ───────────────────────────────────────────────────────────

def fetch_github_trending(language: str = "", limit: int = 5) -> list[dict]:
    """GitHub Trending via l'API non-officielle github-trending-api."""
    try:
        url = "https://api.gitterapp.com/repositories"
        params = {"language": language, "since": "daily"}
        data = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT).json()

        results = []
        for repo in data[:limit]:
            results.append({
                "name":        repo.get("fullname", ""),
                "description": repo.get("description", "—"),
                "stars":       repo.get("stars", 0),
                "url":         f"https://github.com/{repo.get('fullname', '')}",
                "language":    repo.get("language", ""),
            })
        return results
    except Exception:
        # Fallback : DuckDuckGo
        try:
            from core.search import search
            raw = search(f"github trending {language} today", max_results=limit)
            return [{"name": "GitHub Trending", "description": raw, "stars": 0,
                     "url": "https://github.com/trending", "language": language}]
        except Exception as e:
            return [{"name": f"[GitHub Trending indisponible : {e}]",
                     "description": "", "stars": 0, "url": "", "language": ""}]


# ── DeFiLlama ────────────────────────────────────────────────────────────────

def fetch_defi_llama(limit: int = 5) -> list[dict]:
    """Top protocoles DeFi par TVL via l'API DeFiLlama (100% gratuite)."""
    try:
        data = requests.get(
            "https://api.llama.fi/protocols",
            headers=HEADERS, timeout=TIMEOUT
        ).json()

        # Trier par TVL décroissant
        sorted_data = sorted(data, key=lambda x: x.get("tvl", 0), reverse=True)

        results = []
        for p in sorted_data[:limit]:
            tvl = p.get("tvl", 0)
            tvl_fmt = f"${tvl/1e9:.1f}B" if tvl >= 1e9 else f"${tvl/1e6:.0f}M"
            results.append({
                "name":    p.get("name", ""),
                "chain":   p.get("chain", ""),
                "tvl":     tvl_fmt,
                "change":  p.get("change_1d", 0),
                "url":     f"https://defillama.com/protocol/{p.get('slug', '')}",
            })
        return results
    except Exception as e:
        return [{"name": f"[DeFiLlama indisponible : {e}]",
                 "chain": "", "tvl": "", "change": 0, "url": ""}]


# ── Reddit ────────────────────────────────────────────────────────────────────

def fetch_reddit(subreddit: str = "Python", limit: int = 5) -> list[dict]:
    """Hot posts d'un subreddit via l'API JSON publique (sans clé)."""
    try:
        url  = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        data = requests.get(url, headers=HEADERS, timeout=TIMEOUT).json()
        posts = data["data"]["children"]

        return [
            {
                "title": p["data"]["title"],
                "score": p["data"]["score"],
                "url":   f"https://reddit.com{p['data']['permalink']}",
                "flair": p["data"].get("link_flair_text", ""),
            }
            for p in posts
            if not p["data"].get("stickied")
        ][:limit]
    except Exception as e:
        return [{"title": f"[r/{subreddit} indisponible : {e}]",
                 "score": 0, "url": "", "flair": ""}]


# ── Module principal ──────────────────────────────────────────────────────────

class SourcesModule:
    def __init__(self, config):
        from core.ai import AIClient
        self.ai     = AIClient(config)
        self.config = config

    def fetch_all(self, source_filter: str = None) -> dict:
        """Récupère toutes les sources (ou une seule si filtrée)."""
        sources = {}
        sf = (source_filter or "").lower()

        if not sf or sf in ("hn", "hackernews", "hacker"):
            print("   📡 Hacker News…")
            sources["hackernews"] = fetch_hackernews(5)

        if not sf or sf in ("gh", "github"):
            print("   📡 GitHub Trending…")
            sources["github_python"] = fetch_github_trending("python", 5)
            sources["github_js"]     = fetch_github_trending("javascript", 3)

        if not sf or sf in ("defi", "web3", "defillama"):
            print("   📡 DeFiLlama…")
            sources["defi"] = fetch_defi_llama(5)

        if not sf or sf in ("reddit", "r/"):
            print("   📡 Reddit…")
            sources["reddit_python"] = fetch_reddit("Python", 4)
            sources["reddit_termux"] = fetch_reddit("termux", 3)
            sources["reddit_ai"]     = fetch_reddit("artificial", 3)

        return sources

    def _format_raw(self, data: dict) -> str:
        """Formate les données brutes en texte lisible."""
        lines = []

        if "hackernews" in data:
            lines.append("── HACKER NEWS ──────────────────")
            for s in data["hackernews"]:
                lines.append(f"  ▸ [{s['score']}pts] {s['title']}")
                if s["url"]:
                    lines.append(f"    {s['url']}")

        if "github_python" in data or "github_js" in data:
            lines.append("\n── GITHUB TRENDING ──────────────")
            for repo in data.get("github_python", []) + data.get("github_js", []):
                lang = f" [{repo['language']}]" if repo.get("language") else ""
                lines.append(f"  ⭐ {repo['name']}{lang} — {repo['description'][:80]}")

        if "defi" in data:
            lines.append("\n── DEFILLAMA (Top Protocoles) ───")
            for p in data["defi"]:
                chg = p["change"]
                arrow = "🟢" if chg > 0 else "🔴" if chg < 0 else "⚪"
                lines.append(f"  {arrow} {p['name']} ({p['chain']}) — TVL {p['tvl']}  {chg:+.1f}%")

        for key in ("reddit_python", "reddit_termux", "reddit_ai"):
            if key in data:
                name = key.replace("reddit_", "r/")
                lines.append(f"\n── REDDIT {name.upper()} ─────────────────")
                for p in data[key]:
                    lines.append(f"  ▸ [{p['score']}↑] {p['title']}")

        return "\n".join(lines)

    def analyze_and_suggest(self, raw_text: str) -> str:
        """Demande à l'IA d'analyser les sources et suggérer du contenu."""
        prompt = f"""Voici les dernières données des sources de veille pour FuegoDev :

{raw_text}

Analyse ces données et fournis :

🔥 TOP 3 OPPORTUNITÉS DE CONTENU
Pour chaque opportunité :
┌──────────────────────────────────────────
│ 📌 SUJET    : [sujet précis]
│ 🎯 ANGLE    : [angle unique FuegoDev]
│ 📋 FORMAT   : [tweet / thread 3-5 / BIP]
│ ⚡ URGENCE  : [poster maintenant / cette semaine]
│ 🔥 HOOK     : [première ligne du post]
└──────────────────────────────────────────

🗣️ POURQUOI ÇA VA ENGAGER
[Explication courte en 2-3 phrases]

💡 ASTUCE DU JOUR
[Un tip pratique issu de ces données que FuegoDev peut partager]"""

        return self.ai.ask(prompt)

    def run(self, source_filter: str = None):
        print(f"\n⚡ Seven — Sources d'inspiration\n{'─'*52}")

        sf_label = source_filter or "toutes les sources"
        print(f"🌐 Récupération : {sf_label}…\n")

        data     = self.fetch_all(source_filter)
        raw_text = self._format_raw(data)

        print(raw_text)
        print(f"\n{'─'*52}")
        print("🤖 Analyse IA en cours…\n")

        suggestions = self.analyze_and_suggest(raw_text)
        print(suggestions)
