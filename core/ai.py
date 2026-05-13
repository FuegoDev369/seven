"""
Client IA multi-provider pour Seven.

Providers supportés :
  groq      → Llama 3.3 70B  (GRATUIT — recommandé)
  gemini    → Gemini 1.5 Flash (GRATUIT)
  anthropic → Claude Sonnet   (payant — upgrade futur)
"""


class AIClient:
    def __init__(self, config):
        self.config   = config
        self.provider = config.ai_provider
        self.system   = self._build_system()
        self._client  = self._init_client()

    # ── System prompt personnalisé FuegoDev ─────────────────────────────────

    def _build_system(self) -> str:
        c = self.config
        return f"""Tu es Seven, l'agent IA personnel de {c.author_name} ({c.twitter_username}).

Tu l'aides à créer du contenu Twitter/X de haute qualité :
- Style    : {c.content_style}
- Sujets   : {', '.join(c.content_topics)}
- Langue   : {c.language}
- Audience : Développeurs, passionnés Tech, curieux Dev/AI/Web3

Chaque contenu doit être :
✅ Utile — apporte une vraie valeur concrète
✅ Actuel — ancré dans les tendances 2025-2026
✅ Authentique — voix propre à FuegoDev, jamais générique
✅ Original — angle unique, pas du recyclage
✅ Éducatif — simplifier le complexe, rendre accessible
✅ Engageant — hook fort, call-to-action quand pertinent

Bonnes pratiques Twitter : hook en première ligne, concision,
2-3 hashtags max, CTA si pertinent."""

    # ── Init du client selon le provider ────────────────────────────────────

    def _init_client(self):
        if self.provider == 'groq':
            from groq import Groq
            return Groq(api_key=self.config.groq_key)

        elif self.provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=self.config.gemini_key)
            return genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=self.system
            )

        elif self.provider == 'anthropic':
            import anthropic
            return anthropic.Anthropic(api_key=self.config.anthropic_key)

        raise ValueError(f"Provider inconnu : {self.provider}")

    # ── Modèle selon le provider ─────────────────────────────────────────────

    @property
    def _model(self):
        return {
            'groq':      'llama-3.3-70b-versatile',
            'gemini':    'gemini-1.5-flash',
            'anthropic': 'claude-sonnet-4-20250514',
        }[self.provider]

    # ── Requête principale ───────────────────────────────────────────────────

    def ask(self, prompt: str, max_tokens: int = 2000) -> str:
        if self.provider == 'groq':
            return self._ask_groq(prompt, max_tokens)
        elif self.provider == 'gemini':
            return self._ask_gemini(prompt, max_tokens)
        elif self.provider == 'anthropic':
            return self._ask_anthropic(prompt, max_tokens)

    # ── Requête avec contexte web (pour les tendances) ───────────────────────

    def ask_with_context(self, prompt: str, web_context: str, max_tokens: int = 2000) -> str:
        """Intègre les résultats DuckDuckGo dans le prompt."""
        enriched = (
            f"=== CONTEXTE WEB (résultats de recherche récents) ===\n"
            f"{web_context}\n"
            f"=== FIN DU CONTEXTE ===\n\n"
            f"{prompt}"
        )
        return self.ask(enriched, max_tokens)

    # ── Implémentations par provider ─────────────────────────────────────────

    def _ask_groq(self, prompt: str, max_tokens: int) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": self.system},
                {"role": "user",   "content": prompt},
            ]
        )
        return resp.choices[0].message.content

    def _ask_gemini(self, prompt: str, max_tokens: int) -> str:
        resp = self._client.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_tokens}
        )
        return resp.text

    def _ask_anthropic(self, prompt: str, max_tokens: int) -> str:
        resp = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            system=self.system,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text
