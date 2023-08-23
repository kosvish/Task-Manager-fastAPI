from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from app.api.models.user import UserCreateModel
from app.db.database import get_db, User
from app.api.models.user import TokenData, UserResponseModel
import jwt
from app.core.security import SECRET_KEY, ALGORITHM
import datetime
from fastapi.security import OAuth2PasswordBearer

register_router = APIRouter()
login_router = APIRouter()


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("username")
        password: str = payload.get("password")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не зарегестрированны!")
        return TokenData(username=username, password=password)

    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Возникла ошибка при расшифровки вашего токена")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время действия вашего токена истекло")


@register_router.post("/register", response_model=UserResponseModel)
async def register_user(user_data: UserCreateModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким именем уже существует")

    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email-ом уже существует")

    payload = {
        "username": user_data.username,
        "email": user_data.email,
        "password": user_data.password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "password": new_user.password,
            "token": token
            }


@login_router.get("/login")
async def login_user(token: str, db: Session = Depends(get_db)):
    user_data = get_current_user(token)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо зарегестрироваться")

    check_username = db.query(User).filter(User.username == user_data.username).first()
    check_password = db.query(User).filter(User.password == user_data.password).first()

    if not check_password and not check_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имя либо пароль недействительны, "
                                                                             "проверьте правильность указанного токена")

    return {"message": f"С возращением {user_data.username}!"}
