import uuid
from pathlib import Path

from app.domain.enums import AssetKind
from app.models.asset import Asset
from app.repositories.asset import AssetRepository
from app.storage.port import StoragePort


class AssetService:
    def __init__(self, asset_repo: AssetRepository, storage: StoragePort) -> None:
        self._asset_repo = asset_repo
        self._storage = storage

    async def upload(self, user_id: int, kind: AssetKind, filename: str, mime: str, data: bytes) -> Asset:
        safe_name = Path(filename).name
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"
        storage_key = f"{user_id}/{kind.value}/{unique_name}"
        url = await self._storage.save(storage_key, data, mime)
        return await self._asset_repo.create(
            user_id,
            kind=kind,
            filename=filename,
            mime=mime,
            size=len(data),
            storage_key=storage_key,
            url=url,
        )
