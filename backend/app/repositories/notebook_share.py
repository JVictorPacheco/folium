from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums import SharePermission
from app.models.notebook import Notebook
from app.models.notebook_share import NotebookShare


class NotebookShareRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_notebook(self, notebook_id: int) -> list[NotebookShare]:
        result = await self._session.execute(
            select(NotebookShare)
            .where(NotebookShare.notebook_id == notebook_id)
            .options(selectinload(NotebookShare.shared_with))
            .order_by(NotebookShare.created_at)
        )
        return list(result.scalars().all())

    async def list_shared_with_user(self, user_id: int) -> list[NotebookShare]:
        result = await self._session.execute(
            select(NotebookShare)
            .where(NotebookShare.shared_with_user_id == user_id)
            .options(selectinload(NotebookShare.notebook).selectinload(Notebook.tags))
        )
        return list(result.scalars().all())

    async def get(self, share_id: int) -> NotebookShare | None:
        return await self._session.get(NotebookShare, share_id)

    async def get_for_notebook_and_user(self, notebook_id: int, user_id: int) -> NotebookShare | None:
        result = await self._session.execute(
            select(NotebookShare).where(
                NotebookShare.notebook_id == notebook_id,
                NotebookShare.shared_with_user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, notebook_id: int, shared_with_user_id: int, permission: SharePermission
    ) -> NotebookShare:
        existing = await self.get_for_notebook_and_user(notebook_id, shared_with_user_id)
        if existing is not None:
            existing.permission = permission
            await self._session.commit()
            await self._session.refresh(existing, ["shared_with"])
            return existing
        share = NotebookShare(
            notebook_id=notebook_id, shared_with_user_id=shared_with_user_id, permission=permission
        )
        self._session.add(share)
        await self._session.commit()
        await self._session.refresh(share, ["shared_with"])
        return share

    async def delete(self, share: NotebookShare) -> None:
        await self._session.delete(share)
        await self._session.commit()
