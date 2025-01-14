from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Nom de votre Key Vault
key_vault_name = "lucaskeyvaultname"
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Créez un client pour accéder aux secrets du Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

# Récupération des secrets depuis Azure Key Vault
try:
    user = client.get_secret("DB-USER").value
    password = client.get_secret("DB-PASSWORD").value
    host = client.get_secret("DB-HOST").value
    port = client.get_secret("DB-PORT").value
    database = client.get_secret("DB-NAME").value
    ssl_ca = client.get_secret("DB-SSL-CA").value
    print("Secrets récupérés avec succès :")
    print(f"User: {user}")
    print(f"Host: {host}")
    print(f"Database: {database}")
except Exception as e:
    print(f"Erreur lors de la récupération d'un secret: {e}")
    # Vous pouvez gérer l'erreur ici ou utiliser des valeurs par défaut

# Construction de l'URL de connexion
DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?ssl_ca={ssl_ca}"
print(f"URL de connexion construite : {DATABASE_URL}")

# Base de données et moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"ssl_ca": ssl_ca})
print("Connexion à la base de données établie.")

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Charger les variables d'environnement du fichier .env
# load_dotenv()

# Paramètres de connexion à Azure MySQL depuis les variables d'environnement
# user = os.getenv("DB_USER")
# password = os.getenv("DB_PASSWORD")
# host = os.getenv("DB_HOST")
# port = os.getenv("DB_PORT")
# database = os.getenv("DB_NAME")
# ssl_ca = os.getenv("DB_SSL_CA")
