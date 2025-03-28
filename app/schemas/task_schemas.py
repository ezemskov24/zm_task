from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    """
    Базовая схема задачи

    :param datetime_to_do: Дата и время, когда задача должна быть выполнена
    :param task_info: Текст задачи
    """
    datetime_to_do: datetime
    task_info: str


class TaskCreate(TaskBase):
    """
    Схема создания новой задачи

    :param datetime_to_do: Дата и время, когда задача должна быть выполнена
    :param task_info: Текст задачи
    """
    pass


class TaskUpdate(TaskBase):
    """
    Схема для обновления существующей задачи

    :param datetime_to_do: Дата и время, когда задача должна быть выполнена
    :param task_info: Текст задачи
    """
    pass


class TaskResponse(TaskBase):
    """
    Схема, используемая для представления задачи в ответах API

    :param id: id задачи
    :param datetime_to_do: Дата и время, когда задача должна быть выполнена
    :param task_info: Текст задачи
    :param created_at: Время создания задачи
    :param updated_at: Время последнего обновления задачи
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
