from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status

from api.adapters.rest.project import TaskUseCases, ProjectUseCases
from api.adapters.rest.dtos import (
    TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO,
    ProjectCreateDTO, ProjectUpdateDTO, ProjectResponseDTO,
    ErrorResponseDTO
)
from api.core.domain.error import (
    TaskNotFoundException, ProjectNotFoundException,
    TaskAlreadyLinkedException, TaskNotLinkedException,
    TaskDeadlineAfterProjectDeadlineException,
    ProjectCannotBeCompletedException
)
from api.adapters.rest.event import get_task_use_cases, get_project_use_cases

task_router = APIRouter(prefix="/tasks", tags=["tasks"])
project_router = APIRouter(prefix="/projects", tags=["projects"])


@task_router.post("/", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreateDTO,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.create_task(task_data)
    except TaskDeadlineAfterProjectDeadlineException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@task_router.get("/", response_model=List[TaskResponseDTO])
def get_all_tasks(
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    return task_use_cases.get_all_tasks()


@task_router.get("/{task_id}", response_model=TaskResponseDTO)
def get_task(
    task_id: UUID,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.get_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@task_router.put("/{task_id}", response_model=TaskResponseDTO)
def update_task(
    task_id: UUID,
    task_data: TaskUpdateDTO,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.update_task(task_id, task_data)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TaskDeadlineAfterProjectDeadlineException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        success = task_use_cases.delete_task(task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@task_router.patch("/{task_id}/complete", response_model=TaskResponseDTO)
def complete_task(
    task_id: UUID,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.complete_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@project_router.post("/", response_model=ProjectResponseDTO, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreateDTO,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    return project_use_cases.create_project(project_data)


@project_router.get("/", response_model=List[ProjectResponseDTO])
def get_all_projects(
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    return project_use_cases.get_all_projects()


@project_router.get("/{project_id}", response_model=ProjectResponseDTO)
def get_project(
    project_id: UUID,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    try:
        return project_use_cases.get_project(project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@project_router.put("/{project_id}", response_model=ProjectResponseDTO)
def update_project(
    project_id: UUID,
    project_data: ProjectUpdateDTO,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    try:
        return project_use_cases.update_project(project_id, project_data)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    try:
        success = project_use_cases.delete_project(project_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@project_router.get("/{project_id}/tasks", response_model=List[TaskResponseDTO])
def get_project_tasks(
    project_id: UUID,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    try:
        return project_use_cases.get_project_tasks(project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@project_router.post("/{project_id}/tasks/{task_id}/link", response_model=TaskResponseDTO)
def link_task_to_project(
    project_id: UUID,
    task_id: UUID,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.link_task_to_project(task_id, project_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TaskAlreadyLinkedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except TaskDeadlineAfterProjectDeadlineException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@project_router.delete("/{project_id}/tasks/{task_id}/unlink", response_model=TaskResponseDTO)
def unlink_task_from_project(
    project_id: UUID,
    task_id: UUID,
    task_use_cases: TaskUseCases = Depends(get_task_use_cases)
):
    try:
        return task_use_cases.unlink_task_from_project(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TaskNotLinkedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@project_router.patch("/{project_id}/complete", response_model=ProjectResponseDTO)
def complete_project(
    project_id: UUID,
    project_use_cases: ProjectUseCases = Depends(get_project_use_cases)
):
    try:
        return project_use_cases.complete_project(project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ProjectCannotBeCompletedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
