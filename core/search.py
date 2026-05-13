"""
Recherche web gratuite via DuckDuckGo.
Aucune clé API requise.
"""

from duckduckgo_search import DDGS


def search(query: str, max_results: int = 6) -> str:
    """
    Recherche DuckDuckGo et retourne un résumé formaté.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get('title', '')
                body  = r.get('body', '')[:200]
                url   = r.get('href', '')
                results.append(f"• {title}\n  {body}\n  {url}")

        if not results:
            return f"Aucun résultat trouvé pour : {query}"

        return "\n\n".join(results)

    except Exception as e:
        return f"[Recherche indisponible : {e}]"


def search_multi(queries: list[str], max_per_query: int = 4) -> str:
    """
    Lance plusieurs recherches et combine les résultats.
    """
    all_results = []
    for q in queries:
        result = search(q, max_per_query)
        all_results.append(f"🔍 Recherche : '{q}'\n{result}")
    return "\n\n" + "─"*50 + "\n\n".join(all_results)
