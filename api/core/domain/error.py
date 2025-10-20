from typing import Optional
from uuid import UUID


class DomainException(Exception):
    pass


class TaskDeadlineAfterProjectDeadlineException(DomainException):
    def __init__(self, task_id: UUID, project_id: UUID, task_deadline: str, project_deadline: str):
        self.task_id = task_id
        self.project_id = project_id
        self.task_deadline = task_deadline
        self.project_deadline = project_deadline
        super().__init__(
            f"Task {task_id} deadline ({task_deadline}) cannot be after project {project_id} deadline ({project_deadline})"
        )


class ProjectCannotBeCompletedException(DomainException):
    def __init__(self, project_id: UUID, incomplete_tasks_count: int):
        self.project_id = project_id
        self.incomplete_tasks_count = incomplete_tasks_count
        super().__init__(
            f"Project {project_id} cannot be completed. {incomplete_tasks_count} tasks are still incomplete."
        )


class TaskNotFoundException(DomainException):
    def __init__(self, task_id: UUID):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")


class ProjectNotFoundException(DomainException):
    def __init__(self, project_id: UUID):
        self.project_id = project_id
        super().__init__(f"Project {project_id} not found")


class TaskAlreadyLinkedException(DomainException):
    def __init__(self, task_id: UUID, current_project_id: UUID):
        self.task_id = task_id
        self.current_project_id = current_project_id
        super().__init__(
            f"Task {task_id} is already linked to project {current_project_id}"
        )


class TaskNotLinkedException(DomainException):
    def __init__(self, task_id: UUID):
        self.task_id = task_id
        super().__init__(f"Task {task_id} is not linked to any project")
