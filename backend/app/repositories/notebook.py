from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notebook import Notebook
from app.models.tag import Tag


class NotebookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _base_query(self):
        return select(Notebook).options(selectinload(Notebook.tags))

    async def list_by_user(self, user_id: int, tag: str | None = None) -> list[Notebook]:
        stmt = self._base_query().where(Notebook.user_id == user_id)
        if tag:
            stmt = stmt.join(Notebook.tags).where(Tag.name == tag.strip().lower())
        stmt = stmt.order_by(Notebook.updated_at.desc())
        result = await self._session.execute(stmt)
        return list(result.unique().scalars().all())

    async def get(self, notebook_id: int, user_id: int) -> Notebook | None:
        result = await self._session.execute(
            self._base_query().where(Notebook.id == notebook_id, Notebook.user_id == user_id)
        )
        return result.unique().scalar_one_or_none()

    async def get_by_id(self, notebook_id: int) -> Notebook | None:
        result = await self._session.execute(self._base_query().where(Notebook.id == notebook_id))
        return result.unique().scalar_one_or_none()

    async def create(self, user_id: int, **values) -> Notebook:
        notebook = Notebook(user_id=user_id, **values)
        self._session.add(notebook)
        await self._session.commit()
        return await self.get(notebook.id, user_id)

    async def update(self, notebook: Notebook, **values) -> Notebook:
        for key, value in values.items():
            setattr(notebook, key, value)
        await self._session.commit()
        return await self.get(notebook.id, notebook.user_id)

    async def delete(self, notebook: Notebook) -> None:
        await self._session.delete(notebook)
        await self._session.commit()
