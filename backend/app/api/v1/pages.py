from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_content_service, get_page_service
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.page import PageContentOut, PageContentUpdate, PageCreate, PageOut
from app.services.content import ContentService, PageNotFoundError, RevisionConflictError
from app.services.page import PageNotFoundError as PageNotFound
from app.services.page import PageService

router = APIRouter(tags=["pages"])


@router.get("/notebooks/{notebook_id}/pages", response_model=list[PageOut])
async def list_pages(
    notebook_id: int,
    user: User = Depends(get_current_user),
    service: PageService = Depends(get_page_service),
) -> list[PageOut]:
    try:
        return await service.list(notebook_id, user.id)
    except PageNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/notebooks/{notebook_id}/pages", response_model=PageOut, status_code=status.HTTP_201_CREATED)
async def create_page(
    notebook_id: int,
    body: PageCreate,
    user: User = Depends(get_current_user),
    service: PageService = Depends(get_page_service),
) -> PageOut:
    try:
        return await service.create(notebook_id, user.id, body.title)
    except PageNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("/pages/{page_id}", response_model=PageOut)
async def get_page(
    page_id: int,
    user: User = Depends(get_current_user),
    service: PageService = Depends(get_page_service),
) -> PageOut:
    try:
        return await service.get_for_user(page_id, user.id)
    except PageNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.put("/pages/{page_id}/content", response_model=PageContentOut)
async def update_page_content(
    page_id: int,
    body: PageContentUpdate,
    user: User = Depends(get_current_user),
    service: ContentService = Depends(get_content_service),
) -> PageContentOut:
    try:
        page = await service.update(page_id, user.id, body.content_json, body.revision)
    except PageNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except RevisionConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return PageContentOut(revision=page.revision, updated_at=page.updated_at)


@router.delete("/pages/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    page_id: int,
    user: User = Depends(get_current_user),
    service: PageService = Depends(get_page_service),
) -> None:
    try:
        await service.delete(page_id, user.id)
    except PageNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
