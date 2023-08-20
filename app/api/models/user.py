from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    username: constr(min_length=3, max_length=12)
    password: int
    email: EmailStr
