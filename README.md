# Pizza Management System API

Une API RESTful pour la gestion d'une pizzeria, construite avec FastAPI et PostgreSQL.

## Fonctionnalités

- Authentification JWT
- Gestion des utilisateurs et des rôles
- Gestion des pizzas disponnible 
- Gestion des commandes
- Gestion des clients
- Upload et gestion des images
- API documentée avec Swagger UI

## Prérequis

- Python 3.8+
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le repository :
```bash
git clone <repository-url>
cd pizza-management-api
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp config.env.example .env
```
Modifier le fichier `.env` avec vos configurations.

5. Initialiser la base de données :
```bash
# Créer la base de données PostgreSQL
createdb pizza_management

# Initialiser Alembic
alembic init alembic

# Créer la première migration
alembic revision --autogenerate -m "Initial migration"

# Appliquer les migrations
alembic upgrade head
```

## Gestion des Migrations

Le projet utilise Alembic pour gérer les migrations de base de données. Voici les commandes principales :

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description de la migration"

# Appliquer toutes les migrations en attente
alembic upgrade head

# Revenir à la version précédente
alembic downgrade -1

# Voir l'historique des migrations
alembic history

# Voir la version actuelle
alembic current
```

## Démarrage

1. Démarrer le serveur de développement :
```bash
uvicorn app.main:app --reload
```

2. Accéder à la documentation de l'API :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Structure du Projet

```
pizza-management-api/
├── alembic/              # Migrations de base de données
├── app/
│   ├── api/             # Routes API
│   ├── core/            # Configuration et sécurité
│   ├── models/          # Modèles SQLAlchemy
│   ├── schemas/         # Schémas Pydantic
│   └── main.py         # Point d'entrée de l'application
├── tests/              # Tests unitaires et d'intégration
├── .env               # Variables d'environnement
├── config.env.example # Exemple de configuration
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation
```

## Tests

```bash
# Exécuter tous les tests
pytest

# Exécuter les tests avec couverture
pytest --cov=app tests/
```

## Déploiement

1. Configurer les variables d'environnement de production
2. Construire l'image Docker :
```bash
docker build -t pizza-management-api .
```

3. Exécuter le conteneur :
```bash
docker run -d -p 8000:8000 pizza-management-api
```

## Sécurité

- Authentification JWT
- Hachage des mots de passe avec bcrypt
- Validation des données avec Pydantic
- Protection CORS configurable
- Rate limiting
- Validation des fichiers uploadés

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 
