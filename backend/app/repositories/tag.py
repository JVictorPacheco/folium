from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag


class TagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_user(self, user_id: int) -> list[Tag]:
        result = await self._session.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        )
        return list(result.scalars().all())

    async def get_or_create_many(self, user_id: int, names: list[str]) -> list[Tag]:
        normalized: list[str] = []
        seen: set[str] = set()
        for raw in names:
            name = raw.strip().lower()
            if not name or name in seen:
                continue
            seen.add(name)
            normalized.append(name)
        if not normalized:
            return []

        result = await self._session.execute(
            select(Tag).where(Tag.user_id == user_id, Tag.name.in_(normalized))
        )
        existing = {tag.name: tag for tag in result.scalars().all()}

        tags: list[Tag] = []
        for name in normalized:
            tag = existing.get(name)
            if tag is None:
                tag = Tag(user_id=user_id, name=name)
                self._session.add(tag)
            tags.append(tag)
        await self._session.flush()
        return tags
