import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Base
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

key_vault_name = "lucaskeyvaultname"
kv_uri = f"https://{key_vault_name}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

# Récupération des secrets
try:
    user = client.get_secret("DB-USER").value
    password = client.get_secret("DB-PASSWORD").value
    host = client.get_secret("DB-HOST").value
    port = client.get_secret("DB-PORT").value
    database = client.get_secret("DB-NAME").value
    ssl_ca = client.get_secret("DB-SSL-CA").value
    print("Secrets récupérés avec succès.")
except Exception as e:
    print(f"Erreur lors de la récupération des secrets : {e}")
    exit()

DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?ssl_ca={ssl_ca}"
engine = create_engine(DATABASE_URL, connect_args={"ssl_ca": ssl_ca})

cnx = None
try:
    print(f"Tentative de connexion à MySQL sur {host}:{port} avec l'utilisateur {user}.")
    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        ssl_ca=ssl_ca
    )
    if cnx.is_connected():
        print("Connexion réussie à la base de données MySQL.")
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès.")
except Error as e:
    print(f"Erreur de connexion : {e}")
finally:
    if cnx and cnx.is_connected():
        cnx.close()
        print("Connexion fermée.")
