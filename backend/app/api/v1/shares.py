from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_share_service
from app.core.deps import get_current_user
from app.models.notebook_share import NotebookShare
from app.models.user import User
from app.schemas.share import ShareCreate, ShareOut
from app.services.share import (
    ShareNotebookNotFoundError,
    ShareOwnSelfError,
    ShareService,
    ShareUserNotFoundError,
)

router = APIRouter(prefix="/notebooks/{notebook_id}/shares", tags=["shares"])


def _to_out(share: NotebookShare) -> ShareOut:
    return ShareOut(
        id=share.id,
        notebook_id=share.notebook_id,
        email=share.shared_with.email,
        permission=share.permission,
        created_at=share.created_at,
    )


@router.get("", response_model=list[ShareOut])
async def list_shares(
    notebook_id: int,
    user: User = Depends(get_current_user),
    service: ShareService = Depends(get_share_service),
) -> list[ShareOut]:
    try:
        shares = await service.list(notebook_id, user.id)
    except ShareNotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [_to_out(s) for s in shares]


@router.post("", response_model=ShareOut, status_code=status.HTTP_201_CREATED)
async def create_share(
    notebook_id: int,
    body: ShareCreate,
    user: User = Depends(get_current_user),
    service: ShareService = Depends(get_share_service),
) -> ShareOut:
    try:
        share = await service.create(notebook_id, user.id, body.email, body.permission)
    except ShareNotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ShareUserNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ShareOwnSelfError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return _to_out(share)


@router.delete("/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_share(
    notebook_id: int,
    share_id: int,
    user: User = Depends(get_current_user),
    service: ShareService = Depends(get_share_service),
) -> None:
    try:
        await service.delete(notebook_id, user.id, share_id)
    except ShareNotebookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
