from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import Annotated
import auth
from auth import get_current_user


# Créer l'application FastAPI
app = FastAPI()
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
async def user(user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentification Failed")
        return {"User": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





