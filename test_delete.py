import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base  # Importation de UserInDB et Base
from models import Users  # Importation de User
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Paramètres de connexion à Azure MySQL depuis les variables d'environnement
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
ssl_ca = os.getenv("DB_SSL_CA")


# Connexion SQLAlchemy à MySQL
DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?ssl_ca={ssl_ca}"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"ssl_ca": ssl_ca})

try:
    # Connexion à la base de données MySQL avec SSL
    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        ssl_ca=ssl_ca,
        ssl_disabled=False  # Utilisation de SSL
    )

    if cnx.is_connected():
        print("Connexion réussie à la base de données MySQL sur Azure.")

        # Supprimer la table 'users' si elle existe
        Users.__table__.drop(bind=engine)
        print("Table 'users' supprimée avec succès.")

except Error as e:
    print(f"Erreur de connexion : {e}")

finally:
    # Fermer la connexion MySQL si elle est établie
    if cnx.is_connected():
        cnx.close()
        print("Connexion fermée.")
