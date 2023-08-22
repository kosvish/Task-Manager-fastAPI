from fastapi import FastAPI
from app.api.endpoints.users import router

app = FastAPI()

app.include_router(router, prefix="/register")
