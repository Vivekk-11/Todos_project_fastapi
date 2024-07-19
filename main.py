from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dependency_injection = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: dependency_injection):
    return db.query(Todos).all()
