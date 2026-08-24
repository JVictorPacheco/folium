from app.models.notebook import Notebook
from app.repositories.notebook import NotebookRepository


class NotebookNotFoundError(Exception):
    pass


class NotebookService:
    def __init__(self, notebook_repo: NotebookRepository) -> None:
        self._repo = notebook_repo

    async def list(self, user_id: int) -> list[Notebook]:
        return await self._repo.list_by_user(user_id)

    async def create(self, user_id: int, data: dict) -> Notebook:
        return await self._repo.create(user_id, **data)

    async def update(self, notebook_id: int, user_id: int, data: dict) -> Notebook:
        notebook = await self._get_or_404(notebook_id, user_id)
        return await self._repo.update(notebook, **data)

    async def delete(self, notebook_id: int, user_id: int) -> None:
        notebook = await self._get_or_404(notebook_id, user_id)
        await self._repo.delete(notebook)

    async def get(self, notebook_id: int, user_id: int) -> Notebook:
        return await self._get_or_404(notebook_id, user_id)

    async def _get_or_404(self, notebook_id: int, user_id: int) -> Notebook:
        notebook = await self._repo.get(notebook_id, user_id)
        if notebook is None:
            raise NotebookNotFoundError("Caderno não encontrado")
        return notebook
