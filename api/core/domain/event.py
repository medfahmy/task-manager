from datetime import datetime
from typing import Optional
from uuid import UUID
from dataclasses import dataclass


@dataclass
class DomainEvent:
    occurred_at: datetime
    event_id: str


@dataclass
class TaskCompletedEvent(DomainEvent):
    task_id: UUID
    project_id: Optional[UUID] = None


@dataclass
class TaskReopenedEvent(DomainEvent):
    task_id: UUID
    project_id: Optional[UUID] = None


@dataclass
class ProjectCompletedEvent(DomainEvent):
    project_id: UUID


@dataclass
class ProjectReopenedEvent(DomainEvent):
    project_id: UUID


@dataclass
class TaskDeadlineApproachingEvent(DomainEvent):
    task_id: UUID
    deadline: datetime
    hours_remaining: int
    project_id: Optional[UUID] = None
