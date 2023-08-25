from app.api.models.task import TaskCreateModel, TaskResponseModel
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db, Task, User
from sqlalchemy.orm import Session

add_task_router = APIRouter()
get_task_router = APIRouter()
delete_task_router = APIRouter()


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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователя с данным именем не существует")

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


