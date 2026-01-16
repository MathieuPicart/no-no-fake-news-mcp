# 🚫 No No Fake News (NNFN) - V2.0 💎

**No No Fake News** est un analyseur de crédibilité d'actualités ultra-moderne conçu pour évaluer de manière critique l'information en ligne. L'outil utilise l'IA pour analyser le langage, la propagation médiatique et la fiabilité des sources.

## 🚀 Fonctionnalités (Version 2.0)

### 🧠 Analyse Intelligente
- **Analyse Linguistique** : Détection de l'émotivité (NLTK) et de la probabilité de clickbait.
- **Analyse NLP** : Extraction automatique des sujets, personnes et organisations citées (spaCy NER).
- **Propagation Médiatique** : Vérification de la couverture du sujet sur d'autres médias via NewsAPI pour évaluer la viralité.

### 💎 Expérience Premium
- **Design Glassmorphism** : Interface moderne avec effets de transparence et de flou.
- **Skeleton Screens** : Placeholders animés pendant l'analyse pour une perception de performance accrue.
- **Animations Staggered** : Apparition progressive et fluide des cartes de résultats.
- **Trust Score Dynamique** : Cercle de progression SVG animé et code couleur (Rouge/Orange/Vert) intelligent.

### ⚙️ Performance & Data
- **Persistance** : Sauvegarde des analyses en base de données PostgreSQL.
- **Cache Redis** : Accélération des analyses répétées pour une réponse instantanée.
- **Historique** : Consultation des dernières analyses avec prévisualisation rapide.

## 🛠 Stack Technique

- **Backend** : FastAPI (Python 3.10+)
- **IA/NLP** : spaCy (modèle `fr_core_news_md`), NLTK VADER
- **Database** : PostgreSQL & Redis (Cache)
- **Scraping** : Cloudscraper & BeautifulSoup4
- **Frontend** : Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+)

## 📦 Installation & Lancement

1. **Cloner le projet**
   ```bash
   git clone https://github.com/MathieuPicart/no-no-fake-news-mcp.git
   cd no-no-fake-news
   ```

2. **Lancer avec Docker (Recommandé)**
   ```bash
   docker-compose up --build
   ```

3. **Lancement manuel**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

## 🗺 Roadmap

- [x] **Phase 1** : MVP (Calcul de score basique)
- [x] **Phase 2** : Enrichissement (NLP, NewsAPI, PostgreSQL)
- [x] **Phase 2.1** : Refonte Design Premium & Skeletons
- [ ] **Phase 3** : Extension Navigateur (Chrome/Firefox)
- [ ] **Phase 4** : API Publique (Auth & Rate limiting)

## 📄 Licence

Ce projet est la propriété de Mathieu Picart. Tous droits réservés.
