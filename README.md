# ⚡ Seven

> Mon agent IA personnel, construit sur mesure.
> Il pense comme moi et m'aide énormément dans mes projets,
> surtout quand il s'agit de me recentrer.
> Il tourne en local ou sur GitHub Actions — sans risque de fuite de données.

*by FuegoDev — [@ahry369](https://twitter.com/ahry369)*

---

## 🆓 100% Gratuit pour démarrer

| Provider | Modèle | Limite gratuite | Inscription |
|----------|--------|-----------------|-------------|
| **Groq** *(recommandé)* | Llama 3.3 70B | 14 400 req/jour | [console.groq.com](https://console.groq.com) |
| **Gemini** | Gemini 1.5 Flash | 1 500 req/jour | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| Anthropic *(upgrade futur)* | Claude Sonnet | Payant | [console.anthropic.com](https://console.anthropic.com) |

La recherche web fonctionne via **DuckDuckGo** — aucune clé API nécessaire.

---

## ✨ Ce que Seven sait faire

| Commande | Description |
|----------|-------------|
| `ideas`  | Génère des idées de tweets ou threads |
| `write`  | Rédige des tweets / threads / reformate |
| `plan`   | Crée et gère ton calendrier 7 jours |
| `analyze`| Score et améliore tes tweets |
| `trends` | Veille tendances Tech/AI/Web3 (web search) |
| `notify` | Notifications Telegram / Discord |
| `daily`  | Pipeline automatisé (GitHub Actions) |

---

## 🚀 Installation

### Termux (Android)

```bash
pkg install python git
git clone https://github.com/TON_USERNAME/seven.git
cd seven
pip install -r requirements.txt --break-system-packages
cp .env.example .env
nano .env
```

### PC / Mac / Linux

```bash
git clone https://github.com/TON_USERNAME/seven.git
cd seven
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 🔑 Obtenir une clé Groq (2 minutes)

1. Va sur [console.groq.com](https://console.groq.com)
2. Crée un compte (gratuit)
3. **API Keys → Create API Key**
4. Copie la clé dans `.env` : `GROQ_API_KEY=gsk_...`

---

## 💻 Utilisation

```bash
# IDÉES
python main.py ideas
python main.py ideas --topic "Python" -n 3
python main.py ideas --thread

# RÉDACTION
python main.py write --idea "Les bases de Git"
python main.py write --thread --idea "Introduction au Web3"
python main.py write --reformat "Mon ancien tweet..."

# PLANNING
python main.py plan --week
python main.py plan --show

# ANALYSE
python main.py analyze "Mon tweet ici"

# TENDANCES
python main.py trends
python main.py trends --topic "AI"

# NOTIFICATIONS
python main.py notify --test
python main.py notify --daily

# RUN COMPLET (GitHub Actions)
python main.py daily
```

---

## ⚙️ GitHub Actions — Automatisation

Seven tourne tout seul chaque matin à **7h UTC**.

1. Push sur GitHub
2. **Settings → Secrets → Actions** → Ajoute :

| Secret | Valeur |
|--------|--------|
| `GROQ_API_KEY` | Ta clé Groq |
| `TELEGRAM_BOT_TOKEN` | Token du bot |
| `TELEGRAM_CHAT_ID` | Ton Chat ID |

3. **Actions → ⚡ Seven Daily Run → Run workflow** pour tester.

---

## 🗂️ Structure

```
seven/
├── main.py                  ← CLI
├── core/
│   ├── config.py            ← Configuration (.env)
│   ├── ai.py                ← Client IA multi-provider
│   ├── search.py            ← Recherche DuckDuckGo (gratuit)
│   └── database.py          ← SQLite local
├── modules/
│   ├── ideas.py
│   ├── writer.py
│   ├── planner.py
│   ├── analyzer.py
│   └── trends.py
├── notifiers/
│   ├── telegram.py
│   └── discord.py
└── .github/workflows/
    └── daily.yml
```

---

## 🛣️ Roadmap

- [ ] Support OpenRouter (accès à +50 modèles gratuits)
- [ ] Dashboard web local
- [ ] Export planning en Notion
- [ ] Mode batch — semaine de tweets rédigés d'un coup
- [ ] Upgrade vers Anthropic Claude (quand dispo)

---

*Made with ⚡ by FuegoDev — built different.*
