# CV Analyzer API (Backend)

Ce dépôt contient le backend de l'application "Analyseur de CV et Matching d'Offres". Il est responsable de l'extraction des données PDF, de l'évaluation sémantique mathématique, et de l'analyse qualitative par LLM.

## Architecture
- **Framework:** FastAPI (Python 3.9)
- **Extraction PDF:** PyMuPDF (layout-aware)
- **Matching Sémantique (NLP):** `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Analyse IA:** Llama 3 (via Groq API) avec validation stricte Pydantic.

## Prérequis
Avant de lancer l'application, vous devez créer un fichier `.env` à la racine du projet. 

```env
# Obligatoire : Votre clé API Groq
GROQ_API_KEY=gsk_votre_cle_api_ici

# Optionnel : Le modèle utilisé par défaut (modifiez-le pour tester d'autres modèles)
GROQ_MODEL=llama-3.3-70b-versatile
```

## 🚀 Déploiement avec Docker (Recommandé)
L'application est conteneurisée pour garantir un environnement reproductible avec les modèles NLP pré-téléchargés.

```bash
# 1. Construire l'image
docker build -t cv-analyzer-api .

# 2. Lancer le conteneur sur le port 8080
docker run -p 8080:8080 -e GROQ_API_KEY="votre_cle_api" cv-analyzer-api
```

## 💻 Développement Local

Si vous préférez exécuter le code nativement, vous pouvez utiliser les raccourcis `make` ou les scripts bash fournis :

```bash
# Créer le venv et installer les dépendances (runtime + dev)
make init 
# Ou alternativement : ./scripts/setup_venv.sh

# Activer l'environnement
source venv/bin/activate

# Lancer le serveur de développement (Uvicorn)
make run
```

Pour exécuter la suite de tests (vérification du parser PDF, du moteur NLP et du bouclier Pydantic LLM) :
```bash
make test
# Ou alternativement : PYTHONPATH=. venv/bin/python -m pytest
```

## 📖 Utilisation de l'API

L'API expose un endpoint principal documenté via Swagger UI, accessible à l'adresse `http://localhost:8080/docs` lorsque le serveur tourne.

**Endpoint :** `POST /api/v1/analyze`
- **cv_file:** Fichier PDF (multipart/form-data)
- **job_description:** Texte brut (string)

**Réponse (JSON) :** Retourne un score de compatibilité (0-100), les données pour un Radar Chart (1-5), les entités correspondantes/manquantes, et des conseils d'amélioration actionnables.