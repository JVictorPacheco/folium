from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.notebook import Notebook
from app.models.notebook_share import NotebookShare
from app.models.page import Page
from app.models.tag import Tag


class PageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_user(self, user_id: int, tag: str | None = None) -> list[Page]:
        stmt = (
            select(Page)
            .join(Notebook, Notebook.id == Page.notebook_id)
            .outerjoin(
                NotebookShare,
                and_(
                    NotebookShare.notebook_id == Notebook.id,
                    NotebookShare.shared_with_user_id == user_id,
                ),
            )
            .where(or_(Notebook.user_id == user_id, NotebookShare.shared_with_user_id == user_id))
            .options(contains_eager(Page.notebook))
        )
        if tag:
            stmt = stmt.join(Notebook.tags).where(Tag.name == tag.strip().lower())
        result = await self._session.execute(stmt)
        return list(result.unique().scalars().all())

    async def list_by_notebook(self, notebook_id: int) -> list[Page]:
        result = await self._session.execute(
            select(Page).where(Page.notebook_id == notebook_id).order_by(Page.position)
        )
        return list(result.scalars().all())

    async def get(self, page_id: int) -> Page | None:
        return await self._session.get(Page, page_id)

    async def next_position(self, notebook_id: int) -> int:
        result = await self._session.execute(
            select(func.coalesce(func.max(Page.position), 0)).where(Page.notebook_id == notebook_id)
        )
        return int(result.scalar_one()) + 1

    async def create(self, notebook_id: int, title: str, position: int) -> Page:
        page = Page(notebook_id=notebook_id, title=title, position=position)
        self._session.add(page)
        await self._session.commit()
        await self._session.refresh(page)
        return page

    async def save(self, page: Page) -> Page:
        await self._session.commit()
        await self._session.refresh(page)
        return page

    async def delete(self, page: Page) -> None:
        await self._session.delete(page)
        await self._session.commit()
