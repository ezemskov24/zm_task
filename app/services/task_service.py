from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.models.task_models import Task


class TaskService:
    """
    Сервис для работы с задачами
    """

    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
        """
        Создает новую задачу в БД

        :param db: Асинхронная сессия базы данных
        :param task_data: Текст задачи. Ожидается объект типа TaskCreate
        :return: Созданная задача
        """
        new_task = Task(**task_data.model_dump())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task

    @staticmethod
    async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
        """
        Получает задачу по ее id

        :param db: Асинхронная сессия базы данных
        :param task_id: id задачи
        :return: Задача с id или None, если не найдена
        """
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Обновляет данные задачи

        :param db: Асинхронная сессия базы данных
        :param task_id: id задачи, которую нужно обновить
        :param task_data: Обновленный текст задачи. Ожидается объект типа TaskUpdate
        :return: Обновленная задача или None, если задача с данным id не найдена
        """
        task = await TaskService.get_task(db, task_id)
        if not task:
            return None
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def list_tasks(db: AsyncSession) -> List[Task]:
        """
        Получает список всех задач

        :param db: Асинхронная сессия базы данных
        :return: Список задач
        """
        result = await db.execute(select(Task))
        return result.scalars().all()
