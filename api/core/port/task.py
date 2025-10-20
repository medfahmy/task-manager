from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from api.core.domain.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        pass
    
    @abstractmethod
    def get_completed(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_overdue(self) -> List[Task]:
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        pass
