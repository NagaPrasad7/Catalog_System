from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import User
from ..authentication import get_current_user
from ..database import users_collection
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

@router.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users", response_model=List[User])
def get_all_users():
    users = users_collection.find()
    return list(users)


@router.post("/users", response_model=User)
def create_user(user: User):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)

    user_dict = user.dict()
    user_dict["password"] = hashed_password

    inserted_user = users_collection.insert_one(user_dict)

    return user
