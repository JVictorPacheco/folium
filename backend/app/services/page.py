from app.models.page import Page
from app.repositories.page import PageRepository
from app.services.access import AccessLevel, NotebookAccessError, NotebookAccessService


class PageNotFoundError(Exception):
    pass


class PageService:
    def __init__(self, page_repo: PageRepository, access: NotebookAccessService) -> None:
        self._page_repo = page_repo
        self._access = access

    async def list(self, notebook_id: int, user_id: int) -> list[Page]:
        await self._require(notebook_id, user_id, AccessLevel.VIEWER)
        return await self._page_repo.list_by_notebook(notebook_id)

    async def create(self, notebook_id: int, user_id: int, title: str) -> Page:
        await self._require(notebook_id, user_id, AccessLevel.EDITOR)
        position = await self._page_repo.next_position(notebook_id)
        return await self._page_repo.create(notebook_id, title, position)

    async def rename(self, page_id: int, user_id: int, title: str) -> Page:
        page = await self._get_page_or_404(page_id)
        await self._require(page.notebook_id, user_id, AccessLevel.EDITOR)
        page.title = title.strip() or page.title
        return await self._page_repo.save(page)

    async def delete(self, page_id: int, user_id: int) -> None:
        page = await self._get_page_or_404(page_id)
        await self._require(page.notebook_id, user_id, AccessLevel.EDITOR)
        await self._page_repo.delete(page)

    async def get_for_user(self, page_id: int, user_id: int) -> Page:
        page = await self._get_page_or_404(page_id)
        await self._require(page.notebook_id, user_id, AccessLevel.VIEWER)
        return page

    async def _get_page_or_404(self, page_id: int) -> Page:
        page = await self._page_repo.get(page_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        return page

    async def _require(self, notebook_id: int, user_id: int, min_level: AccessLevel) -> None:
        try:
            await self._access.require(notebook_id, user_id, min_level)
        except NotebookAccessError as exc:
            raise PageNotFoundError(str(exc)) from exc
