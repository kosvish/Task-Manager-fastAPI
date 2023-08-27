from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api.models.user import UserCreateModel
from app.db.database import get_db, User
import jwt
from app.core.security import SECRET_KEY, ALGORITHM
import datetime
from fastapi.security import OAuth2PasswordBearer

register_router = APIRouter()
login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get("sub")
        username: str = payload.get("username")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не зарегестрированны!",
                                headers={"WWW-Authenticate": "Bearer"})
        return user_id, username

    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Возникла ошибка при расшифровки вашего токена",
                            headers={"WWW-Authenticate": "Bearer"}
                            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время действия вашего токена истекло",
                            headers={"WWW-Authenticate": "Bearer"}
                            )


@register_router.post("/register")
async def register_user(user_data: UserCreateModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким именем уже существует")

    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email-ом уже существует")

    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    payload = {
        "username": user_data.username,
        "email": user_data.email,
        "password": user_data.password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "sub": new_user.id
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return {
        "username": new_user.username,
        "email": new_user.email,
        "password": new_user.password,
        "token": token
    }


@login_router.get("/login")
async def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.username == username).first()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходимо зарегестрироваться")

    check_username = db.query(User).filter(User.username == username).first()
    check_password = db.query(User).filter(User.password == password).first()

    if not check_password or not check_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имя либо пароль недействительны, "
                                                                             "проверьте правильность указанных данных")

    return {"message": f"С возращением {username}!"}
