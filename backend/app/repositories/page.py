from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notebook import Notebook
from app.models.page import Page


class PageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_notebook(self, notebook_id: int) -> list[Page]:
        result = await self._session.execute(
            select(Page).where(Page.notebook_id == notebook_id).order_by(Page.position)
        )
        return list(result.scalars().all())

    async def get(self, page_id: int) -> Page | None:
        return await self._session.get(Page, page_id)

    async def get_for_user(self, page_id: int, user_id: int) -> Page | None:
        result = await self._session.execute(
            select(Page)
            .join(Notebook, Notebook.id == Page.notebook_id)
            .where(Page.id == page_id, Notebook.user_id == user_id)
        )
        return result.scalar_one_or_none()

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
