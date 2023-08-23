from fastapi import FastAPI
from app.api.endpoints.users import register_router, login_router

app = FastAPI()

app.include_router(register_router, prefix="/register")
app.include_router(login_router, prefix="/login")