from app.api.models.task import TaskCreateModel, TaskResponseModel, TaskUpdateModel
from fastapi import APIRouter, Depends, HTTPException, status
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
html_router = APIRouter()

def check_user(username: str, db: Session = Depends(get_db)):
    check_username = db.query(User).filter(User.username == username).first()
    if not check_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    return True
    pass


@add_task_router.post("/{username}/add_task", response_model=TaskResponseModel)
async def add_task(task: TaskCreateModel, username: str, db: Session = Depends(get_db)):
    check_username = db.query(User).filter(User.username == username).first()
    if not check_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    user_id = check_username.id
    task_data = task.dict()
    task_data["user_id"] = user_id
    new_task = Task(**task_data)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@get_task_router.get("/{username}/get_task")
async def get_task(username: str, db: Session = Depends(get_db)):
    check_user_db = db.query(User).filter(User.username == username).first()
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")
    user_id = check_user_db.id

    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return tasks


@delete_task_router.delete("/{username}/delete_task/{task_id}")
async def delete_task(username: str, task_id: int, db: Session = Depends(get_db)):
    check_user_db = db.query(User).filter(User.username == username).first()
    if not check_user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи с таким id не существует")

    db.delete(task)
    db.commit()
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Задача успешно удалена")


@put_task_router.put("/{username}/update_task/{task_id}", response_model=TaskResponseModel)
async def put_task(username: str, task_id: int, completed: bool, db: Session = Depends(get_db)):
    check_user_db = db.query(User).filter(User.username == username).first()
    if not check_user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователя с данным именем не существует")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Задачи с таким id не существует")

    task.completed = completed

    db.commit()

    return TaskResponseModel(id=task.id, title=task.title, description=task.description, user_id=task.user_id,
                             completed=task.completed)


@html_router.get("/tasks", response_class=HTMLResponse)
async def get_html_template(request: Request, db: Session = Depends(get_db),
                            current_user: UserResponseModel = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user[0]).all()

    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})
