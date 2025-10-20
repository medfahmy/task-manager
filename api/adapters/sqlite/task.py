from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.adapters.sqlite.db import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    project_id = Column(CHAR(36), ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  
    project = relationship("ProjectModel", back_populates="tasks")

    def to_domain(self) -> 'Task':
        from api.core.domain.task import Task, TaskStatus
        return Task(
            id=UUID(self.id),
            title=self.title,
            description=self.description,
            deadline=self.deadline,
            status=TaskStatus.COMPLETED if self.completed else TaskStatus.OPEN,
            project_id=UUID(self.project_id) if self.project_id else None,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, task: 'Task') -> 'TaskModel':
        return cls(
            id=str(task.id),
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            completed=task.is_completed(),
            project_id=str(task.project_id) if task.project_id else None,
            created_at=task.created_at,
            updated_at=task.updated_at
        )


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(255), nullable=False)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

  
    tasks = relationship("TaskModel", back_populates="project")

    def to_domain(self) -> 'Project':
        from api.core.domain.task import Project, ProjectStatus
        return Project(
            id=UUID(self.id),
            title=self.title,
            deadline=self.deadline,
            status=ProjectStatus.COMPLETED if self.completed else ProjectStatus.OPEN,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, project: 'Project') -> 'ProjectModel':
        return cls(
            id=str(project.id),
            title=project.title,
            deadline=project.deadline,
            completed=project.is_completed(),
            created_at=project.created_at,
            updated_at=project.updated_at
        )
