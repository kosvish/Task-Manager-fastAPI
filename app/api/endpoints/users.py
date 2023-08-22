from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api.models.user import UserCreateModel
from app.db.database import get_db, User
from app.api.models.user import UserResponseModel

router = APIRouter()


@router.post("/register", response_model=UserResponseModel)
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

    return new_user
