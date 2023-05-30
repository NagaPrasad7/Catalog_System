import jwt
from fastapi import Depends, HTTPException, status
from .security import verify_password, create_access_token
from .database import users_collection
from .configuration import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})

    if user and verify_password(password, user["password"]):
        token = create_access_token({"sub": str(user["_id"])})
        return {"user": user, "token": token}

    return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub", None)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user = users_collection.find_one({"_id": user_id})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


