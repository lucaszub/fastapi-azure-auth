# 🚀 Authentification avec FastAPI et Azure

Bienvenue dans mon projet personnel dédié à l'implémentation d'un système d'authentification sécurisé avec **FastAPI** et **Azure**.
Ce projet vise à approfondir mes compétences en sécurité et à créer une base réutilisable pour mes futurs projets.

## 📝 Objectifs du projet

- **Comprendre les concepts de sécurité** comme les tokens JWT et la gestion des permissions.
- **Créer une architecture simple et réutilisable** pour intégrer l'authentification dans mes applications futures.

## 🔧 Technologies utilisées

- FastAPI : Framework moderne pour créer des APIs rapides et sécurisées en Python.
- JWT (JSON Web Tokens) : Utilisé pour la gestion des sessions utilisateurs.
- MySQL : Base de données pour stocker les informations utilisateurs.
- Azure : Déploiement sur Azure Web App et gestion des secrets avec Azure Key Vault.
- GitHub Actions : Pour l'automatisation du déploiement.
- Microsoft Entra ID : Pour l'intégration avec l'authentification d'entreprise.

## 📈 Avancements

- Base de données MySQL sur Azure Database for MySQL.
- Système d'authentification en local avec FastAPI.
- Gestion des tokens JWT pour sécuriser les connexions.

## 🛠 À venir

- Azure Key Vault pour sécuriser les secrets.
- Automatisation des déploiements avec GitHub Actions.
- Gestion des utilisateurs avec différents niveaux d'accès (admin, utilisateur standard).
- Déploiement de l'API sur Azure Web App.
  è Déploiement complet de l'application sur Azure avec l'intégration continue.
- Amélioration de la gestion des erreurs et des validations dans l'API.
- Ajout de tests unitaires pour garantir la stabilité de l'application.

## 📂 Structure du projet

```graphql
Copier le code
├── app/ # Dossier contenant le code source de l'API
│ ├── main.py # Point d'entrée de l'application FastAPI
│ ├── models/ # Modèles de données SQLAlchemy
│ ├── schemas/ # Schémas Pydantic pour les requêtes et réponses
│ └── services/ # Logique métier (authentification, gestion des tokens)
├── requirements.txt # Dépendances Python
├── .github/ # Dossier GitHub Actions pour CI/CD
│ └── workflows/
│ └── deploy.yml # Workflow pour déployer l'application
└── README.md # Ce fichier
```

## 📥 Installation et utilisation

1. Cloner le dépôt

```bash
git clone https://github.com/ton-compte/nom-du-depot.git
cd nom-du-depot
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement

- Crée un fichier .env à la racine du projet et ajoute les variables nécessaires (exemple : DATABASE_URL, SECRET_KEY).

4. Lancer l'application

- L'API sera disponible à http://localhost:8000.
- La documentation interactive de l'API sera disponible à http://localhost:8000/docs.

## 📧 Contact

Lucas Zubiarrain - zubiarrainlucas@gmail.com
