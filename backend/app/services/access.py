from enum import IntEnum

from app.models.notebook import Notebook
from app.repositories.notebook import NotebookRepository
from app.repositories.notebook_share import NotebookShareRepository


class AccessLevel(IntEnum):
    VIEWER = 0
    EDITOR = 1
    OWNER = 2

    @property
    def role_name(self) -> str:
        return {AccessLevel.OWNER: "owner", AccessLevel.EDITOR: "editor", AccessLevel.VIEWER: "viewer"}[self]


class NotebookAccessError(Exception):
    pass


class NotebookAccessService:
    """Ponto único de checagem de acesso a um caderno: dono tem acesso total;
    usuário com compartilhamento tem o nível (`viewer`/`editor`) daquele
    registro; qualquer outro usuário não tem acesso nenhum (mesmo tratamento
    de "não encontrado" já usado no isolamento por dono)."""

    def __init__(self, notebook_repo: NotebookRepository, share_repo: NotebookShareRepository) -> None:
        self._notebook_repo = notebook_repo
        self._share_repo = share_repo

    async def resolve(self, notebook_id: int, user_id: int) -> tuple[Notebook, AccessLevel] | None:
        notebook = await self._notebook_repo.get_by_id(notebook_id)
        if notebook is None:
            return None
        if notebook.user_id == user_id:
            return notebook, AccessLevel.OWNER
        share = await self._share_repo.get_for_notebook_and_user(notebook_id, user_id)
        if share is None:
            return None
        level = AccessLevel.EDITOR if share.permission == "editor" else AccessLevel.VIEWER
        return notebook, level

    async def require(self, notebook_id: int, user_id: int, min_level: AccessLevel) -> tuple[Notebook, AccessLevel]:
        result = await self.resolve(notebook_id, user_id)
        if result is None or result[1] < min_level:
            raise NotebookAccessError("Caderno não encontrado")
        return result
