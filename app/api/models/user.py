from typing import List

from pydantic import BaseModel, constr, EmailStr
import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.database import CheckUserInDatabase, SessionLocal
from fastapi import HTTPException, status
from .task import Task

check_user = CheckUserInDatabase()


class UserModel(BaseModel):
    username: constr(min_length=3, max_length=12)
    email: EmailStr
    tasks: List[Task]

    def verify_token(self, token):
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует")

        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
            username = payload.get("sub")
            user = check_user.get_user_by_name(SessionLocal, username)

            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Пользователь не найден, проверьте правильность ввведенных данных")

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")

        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="токен не действителен")


class UserCreateModel(BaseModel):
    username: constr(min_length=3, max_length=12)
    password: constr(min_length=6)
    email: EmailStr


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str



