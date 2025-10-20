from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    project_id: Optional[UUID] = None


class TaskUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class TaskResponseDTO(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: bool
    project_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    deadline: Optional[datetime] = None


class ProjectUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    deadline: Optional[datetime] = None


class ProjectResponseDTO(BaseModel):
    id: UUID
    title: str
    deadline: Optional[datetime] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskLinkDTO(BaseModel):
    task_id: UUID
    project_id: UUID


class ErrorResponseDTO(BaseModel):
    error: str
    detail: Optional[str] = None
