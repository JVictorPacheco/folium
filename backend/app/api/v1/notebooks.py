from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_notebook_service
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.notebook import NotebookCreate, NotebookOut, NotebookUpdate
from app.services.notebook import NotebookNotFoundError, NotebookService

router = APIRouter(prefix="/notebooks", tags=["notebooks"])


@router.get("", response_model=list[NotebookOut])
async def list_notebooks(
    user: User = Depends(get_current_user),
    service: NotebookService = Depends(get_notebook_service),
) -> list[NotebookOut]:
    return await service.list(user.id)


@router.post("", response_model=NotebookOut, status_code=status.HTTP_201_CREATED)
async def create_notebook(
    body: NotebookCreate,
    user: User = Depends(get_current_user),
    service: NotebookService = Depends(get_notebook_service),
) -> NotebookOut:
    return await service.create(user.id, body.model_dump())


@router.get("/{notebook_id}", response_model=NotebookOut)
async def get_notebook(
    notebook_id: int,
    user: User = Depends(get_current_user),
    service: NotebookService = Depends(get_notebook_service),
) -> NotebookOut:
    try:
        return await service.get(notebook_id, user.id)
    except NotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{notebook_id}", response_model=NotebookOut)
async def update_notebook(
    notebook_id: int,
    body: NotebookUpdate,
    user: User = Depends(get_current_user),
    service: NotebookService = Depends(get_notebook_service),
) -> NotebookOut:
    try:
        return await service.update(notebook_id, user.id, body.model_dump(exclude_unset=True))
    except NotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.delete("/{notebook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notebook(
    notebook_id: int,
    user: User = Depends(get_current_user),
    service: NotebookService = Depends(get_notebook_service),
) -> None:
    try:
        await service.delete(notebook_id, user.id)
    except NotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
