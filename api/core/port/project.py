from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from api.core.domain.task import Project


class ProjectRepository(ABC):
    @abstractmethod
    def save(self, project: Project) -> Project:
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Project]:
        pass
    
    @abstractmethod
    def get_completed(self) -> List[Project]:
        pass
    
    @abstractmethod
    def delete(self, project_id: UUID) -> bool:
        pass
