from app.models.notebook import Notebook
from app.models.page import Page
from app.repositories.notebook import NotebookRepository
from app.repositories.page import PageRepository


class PageNotFoundError(Exception):
    pass


class PageService:
    def __init__(self, page_repo: PageRepository, notebook_repo: NotebookRepository) -> None:
        self._page_repo = page_repo
        self._notebook_repo = notebook_repo

    async def list(self, notebook_id: int, user_id: int) -> list[Page]:
        await self._ensure_notebook_owned(notebook_id, user_id)
        return await self._page_repo.list_by_notebook(notebook_id)

    async def create(self, notebook_id: int, user_id: int, title: str) -> Page:
        await self._ensure_notebook_owned(notebook_id, user_id)
        position = await self._page_repo.next_position(notebook_id)
        return await self._page_repo.create(notebook_id, title, position)

    async def delete(self, page_id: int, user_id: int) -> None:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        await self._page_repo.delete(page)

    async def get_for_user(self, page_id: int, user_id: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        return page

    async def _ensure_notebook_owned(self, notebook_id: int, user_id: int) -> Notebook:
        notebook = await self._notebook_repo.get(notebook_id, user_id)
        if notebook is None:
            raise PageNotFoundError("Caderno não encontrado")
        return notebook
