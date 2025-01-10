# FastAPI Azure Authentication Template

Ce projet fournit un template simple pour utiliser l'authentification avec Azure Active Directory dans une application FastAPI, en utilisant SQLAlchemy pour la gestion de la base de données et MySQL sur Azure. Le but est de simplifier l'intégration de l'authentification Azure et de fournir un modèle prêt à l'emploi pour des applications nécessitant cette fonctionnalité.

## Prérequis

Avant de commencer, assurez-vous que vous avez les éléments suivants :

- Un compte Azure et un abonnement actif.
- Un environnement Python (version 3.8 ou supérieure recommandé).
- Azure MySQL ou une autre base de données compatible.
- `pip` pour installer les dépendances.

## Installation

1. **Clonez ce dépôt** sur votre machine locale.

   ```bash
   git clone https://github.com/yourusername/azure-auth-fastapi.git
   cd azure-auth-fastapi
   ```

2. **Créez un environnement virtue** et activez-le.

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installez les dépendances** du projet.

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurez les variables d'environnement**.
   Créez un fichier .env à la racine du projet avec les informations de connexion de votre base de données MySQL Azure.
   Exemple de fichier .env :

   ```makefile
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host
   DB_PORT=3306
   DB_NAME=your_database_name
   DB_SSL_CA=path_to_your_ssl_certificate

   ```

5. **Lancer l'application**
   Démarrez le serveur FastAPI avec Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   L'application sera accessible à http://127.0.0.1:8000.

## Strcture du projet

Voici la structure de base du projet :

```bash
.
├── main.py             # Point d'entrée de l'application FastAPI
├── db_utils.py         # Gestion de la connexion à la base de données Azure
├── models.py           # Modèles de la base de données SQLAlchemy
├── auth.py             # Gestion de l'authentification Azure
├── .env                # Fichier de configuration des variables d'environnement
└── requirements.txt    # Liste des dépendances du projet

```

## Description des fichiers :

- **main.py** : Contient la logique principale de l'application FastAPI et le point d'entrée pour les requêtes HTTP.
- **db_utils.py** : Contient la logique de connexion à la base de données MySQL sur Azure et la configuration de SQLAlchemy.
- **models.py** : Contient les modèles SQLAlchemy pour la base de données, en particulier le modèle Users pour la gestion des utilisateurs.
- **auth.py** : Gère l'authentification Azure, incluant les fonctions pour valider l'utilisateur et sécuriser les endpoints de l'API.
- **.env** : Fichier contenant les variables d'environnement sensibles (comme les informations de connexion à la base de données).

## Utilisation

1. Endpoints disponibles :

- GET /: Retourne les informations de l'utilisateur connecté. Nécessite une authentification via Azure AD. (a développer par la suite

Exemple de requête :

```bash
curl -X 'GET' \
'http://127.0.0.1:8000/' \
-H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

2. **Authentification**:
   Le projet utilise un middleware pour gérer l'authentification Azure. Les utilisateurs doivent s'authentifier via Azure Active Directory pour accéder aux ressources sécurisées.
3. Base de données :
   Ce template utilise MySQL comme base de données pour stocker les informations des utilisateurs. Assurez-vous que la base de données est bien configurée et accessible.

## Contribution

Si vous souhaitez contribuer à ce projet, n'hésitez pas à ouvrir une pull request. Voici quelques points d'amélioration possibles :

- Ajouter des tests unitaires.
- Améliorer la gestion des erreurs.
- Ajouter des fonctionnalités d'autorisation avancées (par exemple, les rôles utilisateur).
