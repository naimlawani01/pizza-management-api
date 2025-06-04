FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers de l'application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port
EXPOSE 8000

# Commande pour démarrer l'application avec migrations
CMD sh -c "echo 'Waiting for database...' && sleep 10 && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000" 