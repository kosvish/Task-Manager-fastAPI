from pydantic import BaseModel, constr, EmailStr


class UserCreateModel(BaseModel):
    username: constr(min_length=3, max_length=12)
    password: constr(min_length=6)
    email: EmailStr


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    token: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    username: str | None = None
    password: str | None = None
