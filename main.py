import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jwt.exceptions import InvalidTokenError
from database import get_db, get_user, create_user_in_db, verify_password, get_password_hash, authenticate_user, UserInDB
from sqlalchemy.orm import Session


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Constantes pour la gestion des tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Définition des Pydantic models pour l'authentification
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    password: str  # Ajout du champ mot de passe

    class Config:
        orm_mode = True

# Modèle Pydantic pour l'utilisateur en base de données
class UserInDBResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

    class Config:
        orm_mode = True

# Fonctions pour la gestion des tokens
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour récupérer l'utilisateur actif à partir du token
def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Décodage du token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
        user = get_user(db, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Routes FastAPI

# Route pour créer un utilisateur
@app.post("/users/", response_model=UserInDBResponse)
async def create_user(
    user: UserCreate, db: Session = Depends(get_db)
):
    # Vérifier si l'utilisateur existe déjà
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hacher le mot de passe avant d'enregistrer dans la base de données
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    
    # Ajouter l'utilisateur à la base de données
    db_user_created = create_user_in_db(db, user_in_db)
    return db_user_created  # Retourne l'objet avec les champs définis dans UserInDBResponse

# Route pour se connecter et obtenir un token d'accès
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Route sécurisée pour récupérer les informations de l'utilisateur connecté
@app.get("/users/me", response_model=UserInDBResponse)
async def read_users_me(current_user: UserInDBResponse = Depends(get_current_active_user)):
    return current_user
