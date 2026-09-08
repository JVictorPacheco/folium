from fastapi import APIRouter, Depends

from app.api.deps import get_tag_service
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.tag import TagOut
from app.services.tag import TagService

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagOut])
async def list_tags(
    user: User = Depends(get_current_user),
    service: TagService = Depends(get_tag_service),
) -> list[TagOut]:
    return await service.list(user.id)
