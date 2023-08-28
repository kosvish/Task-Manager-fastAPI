from fastapi import FastAPI
from app.api.endpoints.users import register_router, login_router
from app.api.endpoints.tasks import (add_task_router, get_task_router, delete_task_router, put_task_router,
                                     html_router_personal_task, dashboard_router)

from app.api.websocket.ws import web_socket_rout
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(add_task_router)
app.include_router(get_task_router)
app.include_router(delete_task_router)
app.include_router(put_task_router)
app.include_router(html_router_personal_task)
app.include_router(dashboard_router)
app.include_router(web_socket_rout)

app.mount("/static", StaticFiles(directory="static"), name="static")
