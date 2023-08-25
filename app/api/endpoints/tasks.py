from app.api.models.task import TaskCreateModel, TaskResponseModel
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db,  Task, User
from sqlalchemy.orm import Session

add_task_router = APIRouter()


def check_user(username: str):
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


