from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    datetime_to_do = Column(DateTime, nullable=False)
    task_info = Column(String, nullable=False)
