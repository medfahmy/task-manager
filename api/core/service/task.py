from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from api.core.domain.task import Task, Project, TaskStatus, ProjectStatus
from api.core.domain.event import (
    TaskCompletedEvent, 
    TaskReopenedEvent, 
    ProjectCompletedEvent, 
    ProjectReopenedEvent,
    TaskDeadlineApproachingEvent
)
from api.core.domain.error import (
    TaskDeadlineAfterProjectDeadlineException,
    ProjectCannotBeCompletedException
)
from api.core.port.task import TaskRepository
from api.core.port.project import ProjectRepository
from api.core.port.event import EventPublisher


class TaskDomainService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository, event_publisher: EventPublisher):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.event_publisher = event_publisher

    def validate_task_deadline(self, task: Task, project_id: Optional[UUID] = None) -> None:
        if not task.deadline or not project_id:
            return
            
        project = self.project_repository.get_by_id(project_id)
        if not project or not project.deadline:
            return
            
        if task.deadline > project.deadline:
            raise TaskDeadlineAfterProjectDeadlineException(
                task.id, 
                project_id, 
                task.deadline.isoformat(), 
                project.deadline.isoformat()
            )

    def complete_task(self, task_id: UUID) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        if task.is_completed():
            return task
            
        task.mark_completed()
        self.task_repository.save(task)
        
      
        self.event_publisher.publish(TaskCompletedEvent(
            occurred_at=datetime.utcnow(),
            event_id=str(uuid4()),
            task_id=task_id,
            project_id=task.project_id
        ))
        
      
        if task.project_id:
            self._check_project_auto_completion(task.project_id)
            
        return task

    def reopen_task(self, task_id: UUID) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        if not task.is_completed():
            return task
            
        task.reopen()
        self.task_repository.save(task)
        
      
        if task.project_id:
            project = self.project_repository.get_by_id(task.project_id)
            if project and project.is_completed():
                project.reopen()
                self.project_repository.save(project)
                
              
                self.event_publisher.publish(ProjectReopenedEvent(
                    occurred_at=datetime.utcnow(),
                    event_id=str(uuid4()),
                    project_id=task.project_id
                ))
        
      
        self.event_publisher.publish(TaskReopenedEvent(
            occurred_at=datetime.utcnow(),
            event_id=str(uuid4()),
            task_id=task_id,
            project_id=task.project_id
        ))
        
        return task

    def _check_project_auto_completion(self, project_id: UUID) -> None:
        auto_complete_projects = True
        
        if not auto_complete_projects:
            return
            
        project = self.project_repository.get_by_id(project_id)
        if not project or project.is_completed():
            return
            
      
        tasks = self.task_repository.get_by_project_id(project_id)
        if all(task.is_completed() for task in tasks):
            project.mark_completed()
            self.project_repository.save(project)
            
          
            self.event_publisher.publish(ProjectCompletedEvent(
                occurred_at=datetime.utcnow(),
                event_id=str(uuid4()),
                project_id=project_id
            ))
