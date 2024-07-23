from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from starlette import status
from passlib.context import CryptContext
from database import SessionLocal

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dependency_injection = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    role: str


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(db: dependency_injection, create_user_request: CreateUserRequest):
    create_user_model = Users(email=create_user_request.email, username=create_user_request.username,
                              first_name=create_user_request.first_name, last_name=create_user_request.last_name,
                              hashed_password=bcrypt_context.hash(create_user_request.password),
                              role=create_user_request.role)

    db.add(create_user_model)
    db.commit()
