from app.api.models.task import TaskCreateModel, TaskResponseModel
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.db.database import get_db, Task, User
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.api.endpoints.users import get_current_user
from app.api.models.user import UserResponseModel
from fastapi.responses import HTMLResponse
from pathlib import Path

templates_directory = Path(__file__).parent.parent.parent / "templates"


add_task_router = APIRouter()
get_task_router = APIRouter()
delete_task_router = APIRouter()
put_task_router = APIRouter()
html_router_personal_task = APIRouter()
dashboard_router = APIRouter()

templates = Jinja2Templates(directory=templates_directory)


@add_task_router.post("/add_task", response_model=TaskResponseModel)
async def add_task(task: TaskCreateModel, db: Session = Depends(get_db),
                   current_user: UserResponseModel = Depends(get_current_user)):
    check_username = db.query(User).filter(User.username == current_user[1]).first()
    if not check_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    task_data = task.dict()
    task_data["user_id"] = current_user[0]
    new_task = Task(**task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@get_task_router.get("/get_task")
async def get_task(db: Session = Depends(get_db), current_user: UserResponseModel = Depends(get_current_user)):
    check_user = db.query(User).filter(User.username == current_user[1]).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")
    user_id = current_user[0]

    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return tasks


@delete_task_router.delete("/delete_task/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db),
                      current_user: UserResponseModel = Depends(get_current_user)):

    check_user_db = db.query(User).filter(User.username == current_user[1]).first()
    if not check_user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task and task.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи с таким id не существует")

    if task.user_id != current_user[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вы не можете удалять чужие задачи")

    db.delete(task)
    db.commit()
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Задача успешно удалена")


@put_task_router.put("/update_task/{task_id}", response_model=TaskResponseModel)
async def put_task(task_id: int, completed: bool,
                   db: Session = Depends(get_db), current_user: UserResponseModel = Depends(get_current_user)):

    check_user_db = db.query(User).filter(User.username == current_user[1]).first()

    if not check_user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Задачи с таким id не существует")

    if task.user_id != current_user[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Вы не можете редактировать чужие задачи"
                            )

    task.completed = completed

    db.commit()

    return TaskResponseModel(id=task.id, title=task.title, description=task.description, user_id=task.user_id,
                             completed=task.completed)


@html_router_personal_task.get("/tasks", response_class=HTMLResponse)
async def get_html_template(request: Request, db: Session = Depends(get_db),
                            current_user: UserResponseModel = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user[0]).all()

    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def get_html_template(request: Request, db: Session = Depends(get_db),
                            current_user: UserResponseModel = Depends(get_current_user)):
    tasks = db.query(Task).all()

    return templates.TemplateResponse("dashboard.html", {"request": request, "tasks": tasks})