from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.verify import verify_token
from app.schemas.task_schemas import TaskResponse, TaskCreate, TaskUpdate
from app.schemas.token_schemas import TokenData
from app.services.task_service import TaskService
from app.core.database import get_db

router: APIRouter = APIRouter(
    prefix='/tasks'
)


@router.get("/list", response_model=List[TaskResponse])
async def list_tasks(
        db: AsyncSession = Depends(get_db),
        token_data: TokenData = Depends(verify_token)
):
    """
    Возвращает список задачи
    """
    return await TaskService.list_tasks(db)


@router.post("/create", response_model=TaskResponse)
async def create_task(
        task: TaskCreate,
        db: AsyncSession = Depends(get_db),
        token_data: TokenData = Depends(verify_token)
):
    """
    Создает задачу
    """
    return await TaskService.create_task(db, task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        token_data: TokenData = Depends(verify_token)
):
    """
    Возвращает задачу по id
    """
    return await TaskService.get_task(db, task_id)


@router.patch("/{task_id}/update", response_model=TaskResponse)
async def update_task(
        task_id: int,
        task: TaskUpdate,
        db: AsyncSession = Depends(get_db),
        token_data: TokenData = Depends(verify_token)
):
    """
    Обновляет задачу
    """
    return await TaskService.update_task(db, task_id, task)
