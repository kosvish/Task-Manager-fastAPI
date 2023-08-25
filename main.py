from fastapi import FastAPI
from app.api.endpoints.users import register_router, login_router
from app.api.endpoints.tasks import add_task_router

app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(add_task_router)
