from app.domain.enums import SharePermission
from app.models.notebook_share import NotebookShare
from app.repositories.notebook_share import NotebookShareRepository
from app.repositories.user import UserRepository
from app.services.access import AccessLevel, NotebookAccessError, NotebookAccessService


class ShareNotebookNotFoundError(Exception):
    pass


class ShareUserNotFoundError(Exception):
    pass


class ShareOwnSelfError(Exception):
    pass


class ShareService:
    def __init__(
        self, share_repo: NotebookShareRepository, user_repo: UserRepository, access: NotebookAccessService
    ) -> None:
        self._share_repo = share_repo
        self._user_repo = user_repo
        self._access = access

    async def list(self, notebook_id: int, owner_id: int) -> list[NotebookShare]:
        await self._require_owner(notebook_id, owner_id)
        return await self._share_repo.list_by_notebook(notebook_id)

    async def create(
        self, notebook_id: int, owner_id: int, email: str, permission: SharePermission
    ) -> NotebookShare:
        await self._require_owner(notebook_id, owner_id)
        target = await self._user_repo.get_by_email(email.strip().lower())
        if target is None:
            raise ShareUserNotFoundError("Não existe usuário cadastrado com esse e-mail")
        if target.id == owner_id:
            raise ShareOwnSelfError("Você já é dono deste caderno")
        return await self._share_repo.upsert(notebook_id, target.id, permission)

    async def delete(self, notebook_id: int, owner_id: int, share_id: int) -> None:
        await self._require_owner(notebook_id, owner_id)
        share = await self._share_repo.get(share_id)
        if share is None or share.notebook_id != notebook_id:
            raise ShareNotebookNotFoundError("Compartilhamento não encontrado")
        await self._share_repo.delete(share)

    async def _require_owner(self, notebook_id: int, owner_id: int) -> None:
        try:
            await self._access.require(notebook_id, owner_id, AccessLevel.OWNER)
        except NotebookAccessError as exc:
            raise ShareNotebookNotFoundError(str(exc)) from exc
