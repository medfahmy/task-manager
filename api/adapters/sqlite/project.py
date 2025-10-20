from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from api.core.domain.task import Task, Project
from api.core.port.task import TaskRepository
from api.core.port.project import ProjectRepository
from api.core.port.event import EventPublisher
from api.adapters.sqlite.task import TaskModel, ProjectModel


class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, task: Task) -> Task:
        task_model = self.db.query(TaskModel).filter(TaskModel.id == str(task.id)).first()
        
        if task_model:
          
            task_model.title = task.title
            task_model.description = task.description
            task_model.deadline = task.deadline
            task_model.completed = task.is_completed()
            task_model.project_id = str(task.project_id) if task.project_id else None
            task_model.updated_at = datetime.utcnow()
        else:
          
            task_model = TaskModel.from_domain(task)
            self.db.add(task_model)
        
        self.db.commit()
        self.db.refresh(task_model)
        return task_model.to_domain()

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        task_model = self.db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
        return task_model.to_domain() if task_model else None

    def get_all(self) -> List[Task]:
        task_models = self.db.query(TaskModel).all()
        return [task.to_domain() for task in task_models]

    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        task_models = self.db.query(TaskModel).filter(TaskModel.project_id == str(project_id)).all()
        return [task.to_domain() for task in task_models]

    def get_completed(self) -> List[Task]:
        task_models = self.db.query(TaskModel).filter(TaskModel.completed == True).all()
        return [task.to_domain() for task in task_models]

    def get_overdue(self) -> List[Task]:
        now = datetime.utcnow()
        task_models = self.db.query(TaskModel).filter(
            TaskModel.deadline < now,
            TaskModel.completed == False
        ).all()
        return [task.to_domain() for task in task_models]

    def delete(self, task_id: UUID) -> bool:
        task_model = self.db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
        if task_model:
            self.db.delete(task_model)
            self.db.commit()
            return True
        return False


class SQLiteProjectRepository(ProjectRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, project: Project) -> Project:
        project_model = self.db.query(ProjectModel).filter(ProjectModel.id == str(project.id)).first()
        
        if project_model:
          
            project_model.title = project.title
            project_model.deadline = project.deadline
            project_model.completed = project.is_completed()
            project_model.updated_at = datetime.utcnow()
        else:
          
            project_model = ProjectModel.from_domain(project)
            self.db.add(project_model)
        
        self.db.commit()
        self.db.refresh(project_model)
        return project_model.to_domain()

    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        project_model = self.db.query(ProjectModel).filter(ProjectModel.id == str(project_id)).first()
        return project_model.to_domain() if project_model else None

    def get_all(self) -> List[Project]:
        project_models = self.db.query(ProjectModel).all()
        return [project.to_domain() for project in project_models]

    def get_completed(self) -> List[Project]:
        project_models = self.db.query(ProjectModel).filter(ProjectModel.completed == True).all()
        return [project.to_domain() for project in project_models]

    def delete(self, project_id: UUID) -> bool:
        project_model = self.db.query(ProjectModel).filter(ProjectModel.id == str(project_id)).first()
        if project_model:
            self.db.delete(project_model)
            self.db.commit()
            return True
        return False


class InMemoryEventPublisher(EventPublisher):
    def __init__(self):
        self.events = []

    def publish(self, event) -> None:
        self.events.append(event)
        print(f"Event published: {type(event).__name__}")

    def get_events(self):
        return self.events.copy()

    def clear_events(self):
        self.events.clear()
