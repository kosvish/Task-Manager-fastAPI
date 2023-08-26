from pydantic import BaseModel
from typing import Optional


class TaskCreateModel(BaseModel):
    title: str
    description: str
    completed: bool = None
    user_id: Optional[int] = None


class TaskResponseModel(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = None


class TaskUpdateModel(BaseModel):
    completed: bool
