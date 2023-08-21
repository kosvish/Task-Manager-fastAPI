from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user = UserModel()


def authenticate_user(token: str = Depends(oauth2_scheme)):
    verify_user = user.verify_token(token)

    if verify_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось аутенфицировать пользователя",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "username": verify_user.username,
        "email": verify_user.email
    }
