# Étape 1 : Construction de l'application
FROM node:18 AS build

WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le code source et construire l'application
COPY . .
RUN npm run build

# Étape 2 : Serveur pour fichiers statiques
FROM node:18-alpine

WORKDIR /app

# Installer serve pour servir les fichiers statiques
RUN npm install -g serve

# Copier le build de l'étape précédente
COPY --from=build /app/dist /app/dist

# Exposer le port 3000 (ou autre port de ton choix)
EXPOSE 3000

# Commande pour lancer le serveur
CMD ["serve", "-s", "dist", "-l", "3000"]
