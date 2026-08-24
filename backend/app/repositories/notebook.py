from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notebook import Notebook


class NotebookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_user(self, user_id: int) -> list[Notebook]:
        result = await self._session.execute(
            select(Notebook)
            .where(Notebook.user_id == user_id)
            .order_by(Notebook.updated_at.desc())
        )
        return list(result.scalars().all())

    async def get(self, notebook_id: int, user_id: int) -> Notebook | None:
        result = await self._session.execute(
            select(Notebook).where(Notebook.id == notebook_id, Notebook.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, **values) -> Notebook:
        notebook = Notebook(user_id=user_id, **values)
        self._session.add(notebook)
        await self._session.commit()
        await self._session.refresh(notebook)
        return notebook

    async def update(self, notebook: Notebook, **values) -> Notebook:
        for key, value in values.items():
            setattr(notebook, key, value)
        await self._session.commit()
        await self._session.refresh(notebook)
        return notebook

    async def delete(self, notebook: Notebook) -> None:
        await self._session.delete(notebook)
        await self._session.commit()
