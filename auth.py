
from dotenv import load_dotenv

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session  
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Nom de votre Key Vault
key_vault_name = "lucaskeyvaultname"
kv_uri = f"https://{key_vault_name}.vault.azure.net"

# Créez un client pour accéder aux secrets du Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# # Charger les variables d'environnement
# load_dotenv()

# # Variables de configuration
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = client.get_secret("SECRET-KEY").value
ALGORITHM = client.get_secret("ALGORITHM").value
# ACCESS_TOKEN_EXPIRE_MINUTES = client.get_secret("ACCESS-TOKEN-EXPIRE-MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_modele = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_modele)
    db.commit()
    
    
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    token = create_acess_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {'access_token': token, 'token_type': 'bearer'}
    

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
        
    
def create_acess_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub":username, "id":user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)   


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

    
    """
Request model for creating a new user.
Attributes:
    username (str): The username of the new user.
    password (str): The password of the new user.
"""
"""
Response model for an access token.
Attributes:
    access_token (str): The JWT access token.
    token_type (str): The type of the token, typically "bearer".
"""
