# Documentation pour le projet d'API FastAPI avec gestion des utilisateurs

## Description du projet

Ce projet utilise **FastAPI** pour créer une API REST simple avec un système d'authentification basé sur des **tokens JWT** et la gestion d'utilisateurs (création de comptes, connexion, récupération des informations de l'utilisateur connecté).

Les fonctionnalités principales incluent :

- **Création de compte** : Permet à un utilisateur de s'enregistrer.
- **Authentification** : Permet à un utilisateur de se connecter avec un nom d'utilisateur et un mot de passe - pour obtenir un token d'accès.
- **Récupération** des informations de l'utilisateur : Permet à un utilisateur de consulter ses informations après s'être authentifié.
- **Vérification de l'authentification** : Les routes protégées nécessitent un token JWT valide pour accéder aux informations.

## Prérequis

- Python 3.10 ou plus récent
  FastAPI
- JWT (via la bibliothèque PyJWT)
- PassLib pour le hachage des mots de passe
- pour la validation des données

## Installation des dépendances

Si tu ne l'as pas encore fait, tu peux installer les dépendances nécessaires via pip :

```bash
pip install fastapi uvicorn passlib pydantic pyjwt
```

## Fonctionnalités

### 1. Création de compte (POST /register/)

Cette route permet de créer un nouvel utilisateur. Elle prend en entrée les informations suivantes :

- username : Le nom d'utilisateur (obligatoire).
- email : L'email de l'utilisateur (obligatoire).
- full_name : Le nom complet de l'utilisateur (optionnel).
- password : Le mot de passe de l'utilisateur (obligatoire).
  **Processus** :
- Vérification que le nom d'utilisateur et l'email ne sont pas déjà utilisés.
- Hachage du mot de passe avec bcrypt.
- Enregistrement de l'utilisateur dans la base de données (un fichier JSON local).
  **Exemple de requête** :

```http
POST /register/
{
  "username": "new_user",
  "email": "new_user@example.com",
  "full_name": "John Doe",
  "password": "my_secure_password"
}

```

**Exemple de réponse** :

```json
{
  "message": "User registered successfully"
}
```

### 2. Connexion et génération de token (POST /token)

Cette route permet à un utilisateur de se connecter en utilisant son **nom d'utilisateur** et **mot de passe** pour obtenir un **token JWT**.

Le token généré est valide pour une durée de 30 minutes par défaut.

**Exemple de requête** :

```http
POST /token
{
  "username": "existing_user",
  "password": "user_password"
}
```

**Exemple de réponse** :

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### 3. Récupérer les informations de l'utilisateur connecté (GET /users/me/)

Cette route permet à l'utilisateur connecté (avec un token valide) de récupérer ses informations personnelles (nom d'utilisateur, email, nom complet, etc.).
**Exemple de requête** :

```http
GET /users/me/
Authorization: Bearer your_jwt_token
```

**Exemple de réponse** :

```json
{
  "username": "existing_user",
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

### 4. Fonctionnalités internes (non exposées par des routes HTTP)

- **Vérification des mots de passe** : Utilisation de **PassLib** pour vérifier les mots de passe avec l'algorithme bcrypt.
- **Hachage des mots de passe** : Les mots de passe sont hachés avant d'être stockés dans la base de données pour garantir la sécurité des utilisateurs.
- **Création et validation des tokens JWT** : Utilisation de la bibliothèque **PyJWT** pour générer un token d'accès lors de la connexion, et vérifier ce token lors des requêtes authentifiées.
- **Gestion de la base de données** : Utilisation d'un fichier JSON (users_db.json) pour stocker les utilisateurs. Ce fichier est chargé et mis à jour à chaque ajout d'utilisateur.

**Fichiers : users_db.json**

Ce fichier stocke les utilisateurs enregistrés sous forme de données JSON. Un utilisateur est représenté par un objet avec les informations suivantes :

- username
- email
- full_name
- hashed_password
- disabled (booléen indiquant si l'utilisateur est actif ou non)

### Fonctionnement détaillé du code

**Authentification via JWT**

- **Génération du token** : Lors de la connexion de l'utilisateur avec /token, un token JWT est généré avec les informations de l'utilisateur et une date d'expiration (par défaut, 30 minutes).
- **Validation du token** : Les requêtes sur les routes protégées (comme /users/me/) nécessitent un token JWT valide. Le token est envoyé dans l'en-tête Authorization de la requête HTTP.

**Gestion des erreurs**

Les erreurs suivantes sont gérées :

- Si l'utilisateur essaie de se connecter avec un nom d'utilisateur ou un mot de passe incorrect, une erreur HTTP_401_UNAUTHORIZED est renvoyée.
- Si un utilisateur essaie d'accéder à une route protégée sans un token valide, une erreur HTTP_401_UNAUTHORIZED est renvoyée.
  **Sauvegarde des utilisateurs**
  Les utilisateurs sont enregistrés dans un fichier JSON local (users_db.json). Le fichier est mis à jour chaque fois qu'un nouvel utilisateur s'enregistre.

### Lancer l'application

```bash
uvicorn main:app --reload
```

Cela démarre le serveur de développement FastAPI à l'adresse http://127.0.0.1:8000.

### Sécurité

- **Gestion des mots de passe** : Les mots de passe sont stockés sous forme de hachage sécurisé (avec bcrypt), jamais en clair.
- **Authentification avec JWT** : Les tokens JWT sont utilisés pour vérifier l'identité de l'utilisateur et sécuriser les endpoints.

---

### Conclusion

Cette API permet de gérer l'inscription et la connexion des utilisateurs avec un système d'authentification sécurisé via JWT. Elle peut être facilement étendue et utilisée comme base pour des applications nécessitant une gestion des utilisateurs.
