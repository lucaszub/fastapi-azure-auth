# db_utils.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
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

# Base de données et moteur
engine = create_engine(DATABASE_URL, connect_args={"ssl_ca": ssl_ca})

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

