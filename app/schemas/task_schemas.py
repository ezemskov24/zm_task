from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    datetime_to_do: datetime
    task_info: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
