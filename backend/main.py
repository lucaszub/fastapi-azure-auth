from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models as models
from database import engine, SessionLocal
from typing import Annotated
import auth as auth
from auth import get_current_user
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


# Créer l'application FastAPI
app = FastAPI()
# Liste des origines autorisées
origins = [
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://authwebappdocker.azurewebsites.net"
    # Ajoute d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser les origines spécifiées
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# @app.get("/hello/")
# def hello_world():
#     return {"hello": "world"}

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: Annotated[dict, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentification Failed")
        return {"User": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))  # Utilisation de la variable d'environnement 'PORT'
    uvicorn.run("main:app", host="0.0.0.0", port=port)





