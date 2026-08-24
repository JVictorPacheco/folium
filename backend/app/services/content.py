from app.models.page import Page
from app.repositories.page import PageRepository


class RevisionConflictError(Exception):
    pass


class PageNotFoundError(Exception):
    pass


class ContentService:
    def __init__(self, page_repo: PageRepository) -> None:
        self._page_repo = page_repo

    async def update(self, page_id: int, user_id: int, content: dict, revision: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        if page.revision != revision:
            raise RevisionConflictError(
                f"Conflito de revisão: esperado {page.revision}, recebido {revision}"
            )
        page.content_json = content
        page.revision += 1
        return await self._page_repo.save(page)

    async def get(self, page_id: int, user_id: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        return page
