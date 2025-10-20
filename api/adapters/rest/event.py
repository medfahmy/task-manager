from sqlalchemy.orm import Session
from fastapi import Depends

from api.adapters.sqlite.db import get_db
from api.adapters.sqlite.project import SQLiteTaskRepository, SQLiteProjectRepository, InMemoryEventPublisher
from api.adapters.rest.project import TaskUseCases, ProjectUseCases


def get_task_repository(db: Session = Depends(get_db)) -> SQLiteTaskRepository:
    return SQLiteTaskRepository(db)


def get_project_repository(db: Session = Depends(get_db)) -> SQLiteProjectRepository:
    return SQLiteProjectRepository(db)


def get_event_publisher() -> InMemoryEventPublisher:
    return InMemoryEventPublisher()


def get_task_use_cases(
    task_repo: SQLiteTaskRepository = Depends(get_task_repository),
    project_repo: SQLiteProjectRepository = Depends(get_project_repository),
    event_publisher: InMemoryEventPublisher = Depends(get_event_publisher)
) -> TaskUseCases:
    return TaskUseCases(task_repo, project_repo, event_publisher)


def get_project_use_cases(
    project_repo: SQLiteProjectRepository = Depends(get_project_repository),
    task_repo: SQLiteTaskRepository = Depends(get_task_repository),
    event_publisher: InMemoryEventPublisher = Depends(get_event_publisher)
) -> ProjectUseCases:
    return ProjectUseCases(project_repo, task_repo, event_publisher)
