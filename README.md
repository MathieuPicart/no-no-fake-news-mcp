# 🚫 No No Fake News (NNFN) - V3.0

**No No Fake News** est un écosystème d'analyse de crédibilité d'actualités conçu pour évaluer de manière critique l'information à l'ère de la désinformation. L'outil combine analyse linguistique, traçage de la propagation médiatique, fact-checking automatisé et une extension navigateur pour une protection en temps réel.

---

## 🚀 Fonctionnalités (Version 3.0)

### 🧠 Moteur d'Analyse Avancé
- **Analyse Linguistique (NLTK)** : Détection automatique du ton émotionnel, de l'emotivité et de la probabilité de clickbait.
- **Analyse NLP (spaCy)** : Extraction d'entités nommées (PER, ORG, GPE) pour une compréhension fine du contexte.
- **Fact-Checking (Google API)** : Interrogation automatique des bases de données de fact-checking pour valider les affirmations.
- **Propagation (NewsAPI)** : Scrutage du volume de mentions et de la viralité de l'information sur les dernières 24h.

### 🛡️ Protection & Accessibilité
- **Extension Navigateur (Manifest V3)** : Un popup pour analyser la crédibilité d'un article en un clic sans quitter votre lecture.
- **Authentification Sécurisée** : Gestion de clés API privées avec Rate Limiting via Redis.
- **Historique Intelligent** : Sauvegarde persistante (PostgreSQL) avec dédoublonnement par URL et accès direct aux rapports détaillés.

### ⚙️ Performance & Robustesse
- **Cache Redis** : Réponses instantanées pour les URLs déjà analysées.
- **Clean Architecture** : Code JavaScript simple.
- **Skeletons Screens** : Expérience utilisateur fluide avec placeholders animés.

---

## 🛠 Stack Technique

- **Backend** : FastAPI (Python 3.10+) 🐍
- **Database** : PostgreSQL (Persistance) & Redis (Cache & Rate Limiting) 🗄️
- **NLP / IA** : spaCy (`fr_core_news_md`), NLTK VADER 🤖
- **Extension** : Chrome/Edge Extension Manifest V3 📦
- **Frontend** : Vanilla HTML5/CSS3, JavaScript 💎

---

## 📦 Installation & Lancement

### 1. Cloner le projet
```bash
git clone https://github.com/MathieuPicart/no-no-fake-news-mcp.git
cd no-no-fake-news
```

### 2. Configuration
Créez un fichier `.env` à la racine. Vous pouvez utiliser le fichier `.env.example` comme modèle.

#### API_KEYS
L'accès aux endpoints de l'API est protégé par une authentification par clé API. Vous pouvez spécifier plusieurs clés API séparées par des virgules. Que vous devrez fournir dans le header de votre requête.
```env
API_KEYS=ma_cle_1,ma_cle_2
```

### 3. Lancement (Docker)
```bash
docker-compose up --build
```

### 4. Lancement (Local)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## ⛩️ Extension Navigateur

Pour installer l'extension en mode développeur :
1. Ouvrez `chrome://extensions/`.
2. Activez le **Mode développeur**.
3. Cliquez sur **Charger l'extension non empaquetée**.
4. Sélectionnez le dossier `/extension/` du projet.

---

## 🗺 Roadmap Accomplie

- [x] **Phase 1** : MVP (Setup & Core Analysis)
- [x] **Phase 2** : Enrichissements (NLP, Database, Cache, Fact-Check)
- [x] **Phase 3** : Extension Navigateur & UI
- [x] **Phase 4** : Sécurité API & Nettoyage de Code

---

## 📄 Licence

Ce projet est la propriété de Mathieu Picart. Tous droits réservés.
