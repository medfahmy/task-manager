from datetime import datetime
from typing import List, Optional
from uuid import UUID

from api.core.domain.task import Task, Project
from api.core.domain.error import (
    TaskNotFoundException, 
    ProjectNotFoundException,
    TaskAlreadyLinkedException,
    TaskNotLinkedException
)
from api.core.service.task import TaskDomainService
from api.core.service.project import ProjectDomainService
from api.core.port.task import TaskRepository
from api.core.port.project import ProjectRepository
from api.core.port.event import EventPublisher
from api.adapters.rest.dtos import (
    TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO,
    ProjectCreateDTO, ProjectUpdateDTO, ProjectResponseDTO
)


class TaskUseCases:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository, 
                 event_publisher: EventPublisher):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.event_publisher = event_publisher
        self.task_domain_service = TaskDomainService(task_repository, project_repository, event_publisher)

    def create_task(self, task_data: TaskCreateDTO) -> TaskResponseDTO:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            project_id=task_data.project_id
        )
        
      
        if task.project_id:
            self.task_domain_service.validate_task_deadline(task, task.project_id)
        
        saved_task = self.task_repository.save(task)
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            deadline=saved_task.deadline,
            completed=saved_task.is_completed(),
            project_id=saved_task.project_id,
            created_at=saved_task.created_at,
            updated_at=saved_task.updated_at
        )

    def get_task(self, task_id: UUID) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        return TaskResponseDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            completed=task.is_completed(),
            project_id=task.project_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    def get_all_tasks(self) -> List[TaskResponseDTO]:
        tasks = self.task_repository.get_all()
        return [
            TaskResponseDTO(
                id=task.id,
                title=task.title,
                description=task.description,
                deadline=task.deadline,
                completed=task.is_completed(),
                project_id=task.project_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

    def update_task(self, task_id: UUID, task_data: TaskUpdateDTO) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.deadline is not None:
            task.update_deadline(task_data.deadline)
          
            if task.project_id:
                self.task_domain_service.validate_task_deadline(task, task.project_id)
        
        saved_task = self.task_repository.save(task)
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            deadline=saved_task.deadline,
            completed=saved_task.is_completed(),
            project_id=saved_task.project_id,
            created_at=saved_task.created_at,
            updated_at=saved_task.updated_at
        )

    def delete_task(self, task_id: UUID) -> bool:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        return self.task_repository.delete(task_id)

    def complete_task(self, task_id: UUID) -> TaskResponseDTO:
        task = self.task_domain_service.complete_task(task_id)
        return TaskResponseDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            completed=task.is_completed(),
            project_id=task.project_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    def link_task_to_project(self, task_id: UUID, project_id: UUID) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        if task.project_id:
            raise TaskAlreadyLinkedException(task_id, task.project_id)
        
      
        if task.deadline:
            self.task_domain_service.validate_task_deadline(task, project_id)
        
        task.link_to_project(project_id)
        saved_task = self.task_repository.save(task)
        
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            deadline=saved_task.deadline,
            completed=saved_task.is_completed(),
            project_id=saved_task.project_id,
            created_at=saved_task.created_at,
            updated_at=saved_task.updated_at
        )

    def unlink_task_from_project(self, task_id: UUID) -> TaskResponseDTO:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        
        if not task.project_id:
            raise TaskNotLinkedException(task_id)
        
        task.unlink_from_project()
        saved_task = self.task_repository.save(task)
        
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            deadline=saved_task.deadline,
            completed=saved_task.is_completed(),
            project_id=saved_task.project_id,
            created_at=saved_task.created_at,
            updated_at=saved_task.updated_at
        )


class ProjectUseCases:
    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository,
                 event_publisher: EventPublisher):
        self.project_repository = project_repository
        self.task_repository = task_repository
        self.event_publisher = event_publisher
        self.project_domain_service = ProjectDomainService(project_repository, task_repository, event_publisher)

    def create_project(self, project_data: ProjectCreateDTO) -> ProjectResponseDTO:
        project = Project(
            title=project_data.title,
            deadline=project_data.deadline
        )
        
        saved_project = self.project_repository.save(project)
        return ProjectResponseDTO(
            id=saved_project.id,
            title=saved_project.title,
            deadline=saved_project.deadline,
            completed=saved_project.is_completed(),
            created_at=saved_project.created_at,
            updated_at=saved_project.updated_at
        )

    def get_project(self, project_id: UUID) -> ProjectResponseDTO:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        return ProjectResponseDTO(
            id=project.id,
            title=project.title,
            deadline=project.deadline,
            completed=project.is_completed(),
            created_at=project.created_at,
            updated_at=project.updated_at
        )

    def get_all_projects(self) -> List[ProjectResponseDTO]:
        projects = self.project_repository.get_all()
        return [
            ProjectResponseDTO(
                id=project.id,
                title=project.title,
                deadline=project.deadline,
                completed=project.is_completed(),
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            for project in projects
        ]

    def update_project(self, project_id: UUID, project_data: ProjectUpdateDTO) -> ProjectResponseDTO:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        if project_data.title is not None:
            project.title = project_data.title
        if project_data.deadline is not None:
            project = self.project_domain_service.update_project_deadline(project_id, project_data.deadline)
        
        saved_project = self.project_repository.save(project)
        return ProjectResponseDTO(
            id=saved_project.id,
            title=saved_project.title,
            deadline=saved_project.deadline,
            completed=saved_project.is_completed(),
            created_at=saved_project.created_at,
            updated_at=saved_project.updated_at
        )

    def delete_project(self, project_id: UUID) -> bool:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        return self.project_repository.delete(project_id)

    def get_project_tasks(self, project_id: UUID) -> List[TaskResponseDTO]:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        
        tasks = self.task_repository.get_by_project_id(project_id)
        return [
            TaskResponseDTO(
                id=task.id,
                title=task.title,
                description=task.description,
                deadline=task.deadline,
                completed=task.is_completed(),
                project_id=task.project_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

    def complete_project(self, project_id: UUID) -> ProjectResponseDTO:
        project = self.project_domain_service.complete_project(project_id)
        return ProjectResponseDTO(
            id=project.id,
            title=project.title,
            deadline=project.deadline,
            completed=project.is_completed(),
            created_at=project.created_at,
            updated_at=project.updated_at
        )
