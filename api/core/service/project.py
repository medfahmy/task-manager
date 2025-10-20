from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from api.core.domain.task import Task, Project
from api.core.domain.event import ProjectCompletedEvent, ProjectReopenedEvent
from api.core.domain.error import ProjectCannotBeCompletedException
from api.core.port.project import ProjectRepository
from api.core.port.task import TaskRepository
from api.core.port.event import EventPublisher


class ProjectDomainService:
    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository, event_publisher: EventPublisher):
        self.project_repository = project_repository
        self.task_repository = task_repository
        self.event_publisher = event_publisher

    def complete_project(self, project_id: UUID) -> Project:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
            
        if project.is_completed():
            return project
            
      
        tasks = self.task_repository.get_by_project_id(project_id)
        incomplete_tasks = [task for task in tasks if not task.is_completed()]
        
        if incomplete_tasks:
            raise ProjectCannotBeCompletedException(
                project_id, 
                len(incomplete_tasks)
            )
            
        project.mark_completed()
        self.project_repository.save(project)
        
      
        self.event_publisher.publish(ProjectCompletedEvent(
            occurred_at=datetime.utcnow(),
            event_id=str(uuid4()),
            project_id=project_id
        ))
        
        return project

    def update_project_deadline(self, project_id: UUID, new_deadline: datetime) -> Project:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
            
        old_deadline = project.deadline
        project.update_deadline(new_deadline)
        
      
        tasks = self.task_repository.get_by_project_id(project_id)
        conflicting_tasks = [
            task for task in tasks 
            if task.deadline and task.deadline > new_deadline
        ]
        
        if conflicting_tasks:
          
            for task in conflicting_tasks:
                task.update_deadline(new_deadline)
                self.task_repository.save(task)
        
        self.project_repository.save(project)
        return project
