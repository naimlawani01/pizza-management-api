# Pizza Management System

Une application web fullstack pour la gestion d'un restaurant de pizzas.

## Fonctionnalités

- Gestion des utilisateurs (Admin, Manager, Staff, Delivery)
- Gestion du menu des pizzas
- Gestion des ingrédients et du stock
- Gestion des commandes
- Gestion des clients
- Système de livraison
- Tableau de bord pour les statistiques

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

2. Créer un environnement virtuel :
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

4. Créer un fichier .env à partir de .env.example et configurer les variables d'environnement :
```bash
cp .env.example .env
```

5. Configurer la base de données PostgreSQL et mettre à jour le DATABASE_URL dans le fichier .env

6. Initialiser la base de données :
```bash
alembic upgrade head
```

## Démarrage

Pour démarrer le serveur de développement :
```bash
uvicorn app.main:app --reload
```

L'API sera disponible à l'adresse : http://localhost:8000
La documentation Swagger sera disponible à l'adresse : http://localhost:8000/docs

## Structure du Projet

```
pizza-management-api/
├── app/
│   ├── api/            # Routes API
│   ├── core/           # Configuration et utilitaires
│   ├── db/             # Configuration de la base de données
│   ├── models/         # Modèles SQLAlchemy
│   ├── schemas/        # Schémas Pydantic
│   └── services/       # Logique métier
├── tests/              # Tests unitaires et d'intégration
├── alembic/            # Migrations de base de données
├── .env                # Variables d'environnement
├── requirements.txt    # Dépendances Python
└── README.md          # Documentation
```

## Tests

Pour exécuter les tests :
```bash
pytest
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. 