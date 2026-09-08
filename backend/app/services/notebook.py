from app.models.notebook import Notebook
from app.repositories.notebook import NotebookRepository
from app.repositories.notebook_share import NotebookShareRepository
from app.repositories.tag import TagRepository
from app.services.access import AccessLevel, NotebookAccessError, NotebookAccessService


class NotebookNotFoundError(Exception):
    pass


class NotebookService:
    def __init__(
        self,
        notebook_repo: NotebookRepository,
        tag_repo: TagRepository,
        share_repo: NotebookShareRepository,
        access: NotebookAccessService,
    ) -> None:
        self._repo = notebook_repo
        self._tag_repo = tag_repo
        self._share_repo = share_repo
        self._access = access

    async def list(self, user_id: int, tag: str | None = None) -> list[Notebook]:
        owned = await self._repo.list_by_user(user_id, tag)
        for notebook in owned:
            notebook.role = AccessLevel.OWNER.role_name
        if tag:
            # Tags são geridas só pelo dono — filtrar por tag não faz sentido
            # sobre cadernos compartilhados, que não têm as tags do dono.
            return owned

        shares = await self._share_repo.list_shared_with_user(user_id)
        shared: list[Notebook] = []
        for share in shares:
            notebook = share.notebook
            notebook.role = AccessLevel.EDITOR.role_name if share.permission == "editor" else AccessLevel.VIEWER.role_name
            shared.append(notebook)
        return owned + shared

    async def create(self, user_id: int, data: dict) -> Notebook:
        notebook = await self._repo.create(user_id, **data)
        notebook.role = AccessLevel.OWNER.role_name
        return notebook

    async def get(self, notebook_id: int, user_id: int) -> Notebook:
        try:
            notebook, level = await self._access.require(notebook_id, user_id, AccessLevel.VIEWER)
        except NotebookAccessError as exc:
            raise NotebookNotFoundError(str(exc)) from exc
        notebook.role = level.role_name
        return notebook

    async def update(self, notebook_id: int, user_id: int, data: dict) -> Notebook:
        notebook = await self._get_owned_or_404(notebook_id, user_id)
        if "tags" in data:
            names = data["tags"] or []
            data["tags"] = await self._tag_repo.get_or_create_many(user_id, names)
        updated = await self._repo.update(notebook, **data)
        updated.role = AccessLevel.OWNER.role_name
        return updated

    async def delete(self, notebook_id: int, user_id: int) -> None:
        notebook = await self._get_owned_or_404(notebook_id, user_id)
        await self._repo.delete(notebook)

    async def _get_owned_or_404(self, notebook_id: int, user_id: int) -> Notebook:
        notebook = await self._repo.get(notebook_id, user_id)
        if notebook is None:
            raise NotebookNotFoundError("Caderno não encontrado")
        return notebook
