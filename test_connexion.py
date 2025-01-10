import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserInDB, Base  # Importation de UserInDB et Base

# Paramètres de connexion à Azure MySQL
user = "zubiarrain"
password = "Medard44"  # Remplace par ton mot de passe
host = "mysqldb-lucas.mysql.database.azure.com"
port = 3306
database = "db-auth-template"  # Remplace par le nom de ta base de données
ssl_ca = "C:/Projet/Cloud-resume/Authentification fast api azure/BaltimoreCyberTrustRoot.crt.pem"  # Chemin vers ton certificat CA

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

        # Création de la table en utilisant SQLAlchemy
        # Cela crée la table 'users' si elle n'existe pas
        Base.metadata.create_all(bind=engine)
        print("Table 'users' créée avec succès.")

except Error as e:
    print(f"Erreur de connexion : {e}")

finally:
    # Fermer la connexion MySQL si elle est établie
    if cnx.is_connected():
        cnx.close()
        print("Connexion fermée.")
