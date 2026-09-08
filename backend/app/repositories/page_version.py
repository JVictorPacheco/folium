from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notebook import Notebook
from app.models.page import Page
from app.models.page_version import PageVersion

RETENTION_LIMIT = 50


class PageVersionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_page_for_user(self, page_id: int, user_id: int) -> list[PageVersion]:
        result = await self._session.execute(
            select(PageVersion)
            .join(Page, Page.id == PageVersion.page_id)
            .join(Notebook, Notebook.id == Page.notebook_id)
            .where(PageVersion.page_id == page_id, Notebook.user_id == user_id)
            .order_by(PageVersion.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_for_user(self, version_id: int, user_id: int) -> PageVersion | None:
        result = await self._session.execute(
            select(PageVersion)
            .join(Page, Page.id == PageVersion.page_id)
            .join(Notebook, Notebook.id == Page.notebook_id)
            .where(PageVersion.id == version_id, Notebook.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def has_recent(self, page_id: int, since: datetime) -> bool:
        result = await self._session.execute(
            select(PageVersion.id)
            .where(PageVersion.page_id == page_id, PageVersion.created_at > since)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, page_id: int, content_json: dict, revision: int) -> PageVersion:
        version = PageVersion(page_id=page_id, content_json=content_json, revision=revision)
        self._session.add(version)
        await self._session.commit()
        await self._session.refresh(version)
        return version

    async def prune(self, page_id: int, keep: int = RETENTION_LIMIT) -> None:
        result = await self._session.execute(
            select(PageVersion.id)
            .where(PageVersion.page_id == page_id)
            .order_by(PageVersion.created_at.desc())
            .offset(keep)
        )
        stale_ids = [row[0] for row in result.all()]
        if stale_ids:
            await self._session.execute(delete(PageVersion).where(PageVersion.id.in_(stale_ids)))
            await self._session.commit()
