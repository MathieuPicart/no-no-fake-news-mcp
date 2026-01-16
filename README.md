# 🚫 No No Fake News (NNFN)

**No No Fake News** est un analyseur de crédibilité d'actualités conçu pour aider les utilisateurs à évaluer de manière critique l'information en ligne. L'outil analyse le langage émotionnel, détecte les clickbaits et évalue la fiabilité des sources.

## 🚀 Fonctionnalités (Phase 1 - MVP)

- **Analyse Linguistique** : Détection de l'émotivité (NLTK VADER) et du clickbait (titres sensationnalistes, majuscules).
- **Vérification des Sources** : Scoring basé sur la réputation du domaine et la présence d'un auteur.
- **Scoring de Crédibilité** : Algorithme pondéré (0-100) avec badges visuels (Rouge, Orange, Vert).
- **Interface Moderne** : Dashboard responsive avec visualisations des métriques.

## 🛠 Stack Technique

- **Backend** : FastAPI (Python)
- **NLP** : NLTK, spaCy
- **Scraping** : Cloudscraper (pour contourner les anti-bots) + BeautifulSoup4
- **Frontend** : Vanille HTML/CSS/JS

## 📦 Installation & Lancement

1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-compte/no-no-fake-news.git
   cd no-no-fake-news
   ```

2. **Setup l'environnement**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Lancer le serveur**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗺 Roadmap

- [x] MVP : Analyse basique et interface web
- [ ] Phase 2 : Intégration Google Fact Check API & NewsAPI
- [ ] Phase 2 : Persistance des données (PostgreSQL)
- [ ] Phase 3 : Extension navigateur

## 📄 Licence

Ce projet est à but éducatif.
