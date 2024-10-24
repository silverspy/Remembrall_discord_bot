# Utiliser une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY . .

# Créer un volume pour la base de données persistante
VOLUME ["/app/data"]

# Exposer un port si nécessaire (ex : si tu utilises un serveur web)
# EXPOSE 8000

# Commande pour lancer le bot
CMD ["python", "bot.py"]
