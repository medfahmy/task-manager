from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    OPEN = "open"
    COMPLETED = "completed"


class ProjectStatus(Enum):
    OPEN = "open"
    COMPLETED = "completed"


@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: TaskStatus = TaskStatus.OPEN
    project_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_completed(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def reopen(self) -> None:
        self.status = TaskStatus.OPEN
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED

    def link_to_project(self, project_id: UUID) -> None:
        self.project_id = project_id
        self.updated_at = datetime.utcnow()

    def unlink_from_project(self) -> None:
        self.project_id = None
        self.updated_at = datetime.utcnow()

    def update_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline
        self.updated_at = datetime.utcnow()


@dataclass
class Project:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    deadline: Optional[datetime] = None
    status: ProjectStatus = ProjectStatus.OPEN
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_completed(self) -> None:
        self.status = ProjectStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def reopen(self) -> None:
        self.status = ProjectStatus.OPEN
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        return self.status == ProjectStatus.COMPLETED

    def update_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline
        self.updated_at = datetime.utcnow()
