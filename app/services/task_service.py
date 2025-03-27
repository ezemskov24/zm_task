from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.models.task_models import Task


class TaskService:
    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
        new_task = Task(**task_data.model_dump())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task


    @staticmethod
    async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()


    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
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
        result = await db.execute(select(Task))
        return result.scalars().all()
