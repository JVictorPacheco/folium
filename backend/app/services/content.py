from datetime import datetime, timedelta, timezone

from app.models.page import Page
from app.models.page_version import PageVersion
from app.repositories.page import PageRepository
from app.repositories.page_version import PageVersionRepository

SNAPSHOT_THROTTLE_MINUTES = 5


class RevisionConflictError(Exception):
    pass


class PageNotFoundError(Exception):
    pass


class PageVersionNotFoundError(Exception):
    pass


class ContentService:
    def __init__(self, page_repo: PageRepository, version_repo: PageVersionRepository) -> None:
        self._page_repo = page_repo
        self._version_repo = version_repo

    async def update(self, page_id: int, user_id: int, content: dict, revision: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        if page.revision != revision:
            raise RevisionConflictError(
                f"Conflito de revisão: esperado {page.revision}, recebido {revision}"
            )
        await self._snapshot_if_due(page)
        page.content_json = content
        page.revision += 1
        return await self._page_repo.save(page)

    async def get(self, page_id: int, user_id: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        return page

    async def list_versions(self, page_id: int, user_id: int) -> list[PageVersion]:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        return await self._version_repo.list_by_page_for_user(page_id, user_id)

    async def get_version(self, page_id: int, version_id: int, user_id: int) -> PageVersion:
        version = await self._version_repo.get_for_user(version_id, user_id)
        if version is None or version.page_id != page_id:
            raise PageVersionNotFoundError("Versão não encontrada")
        return version

    async def restore(self, page_id: int, version_id: int, user_id: int) -> Page:
        page = await self._page_repo.get_for_user(page_id, user_id)
        if page is None:
            raise PageNotFoundError("Página não encontrada")
        version = await self._version_repo.get_for_user(version_id, user_id)
        if version is None or version.page_id != page_id:
            raise PageVersionNotFoundError("Versão não encontrada")

        # snapshot do estado atual antes de sobrescrever, pra restaurar não ser destrutivo
        await self._version_repo.create(page.id, page.content_json, page.revision)
        await self._version_repo.prune(page.id)

        page.content_json = version.content_json
        page.revision += 1
        return await self._page_repo.save(page)

    async def _snapshot_if_due(self, page: Page) -> None:
        since = datetime.now(timezone.utc) - timedelta(minutes=SNAPSHOT_THROTTLE_MINUTES)
        if await self._version_repo.has_recent(page.id, since):
            return
        await self._version_repo.create(page.id, page.content_json, page.revision)
        await self._version_repo.prune(page.id)
