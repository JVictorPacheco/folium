from app.models.tag import Tag
from app.repositories.tag import TagRepository


class TagService:
    def __init__(self, tag_repo: TagRepository) -> None:
        self._repo = tag_repo

    async def list(self, user_id: int) -> list[Tag]:
        return await self._repo.list_by_user(user_id)
