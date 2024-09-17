# Utiliser une image de base Python slim
FROM python:3.8-slim

# Mise à jour des packages et installation des dépendances système nécessaires
RUN apt-get update -y && apt-get install -y libpq-dev gcc

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du répertoire de travail actuel dans le conteneur
COPY .  .



# Installer les dépendances Python
RUN pip install -r requirements.txt
# Installer Alembic
RUN pip install alembic
