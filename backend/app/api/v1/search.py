from fastapi import APIRouter, Depends, Query

from app.api.deps import get_search_service
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.search import SearchResult
from app.services.search import SearchService

router = APIRouter(tags=["search"])


@router.get("/search", response_model=list[SearchResult])
async def search(
    q: str = Query(..., min_length=1),
    tag: str | None = Query(None),
    user: User = Depends(get_current_user),
    service: SearchService = Depends(get_search_service),
) -> list[SearchResult]:
    return await service.search(user.id, q, tag)
