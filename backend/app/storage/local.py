import asyncio
from pathlib import Path

from app.core.config import settings
from app.storage.port import StoragePort


class LocalStorage(StoragePort):
    def __init__(self, base_dir: str | None = None) -> None:
        self._base = Path(base_dir or settings.storage_dir)

    def _path(self, key: str) -> Path:
        safe_key = key.replace("\\", "/")
        return self._base / safe_key

    async def save(self, key: str, data: bytes, content_type: str) -> str:
        path = self._path(key)
        await asyncio.to_thread(self._write, path, data)
        return f"{settings.media_url_prefix}/{key}"

    async def delete(self, key: str) -> None:
        path = self._path(key)
        await asyncio.to_thread(self._remove, path)

    @staticmethod
    def _write(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    @staticmethod
    def _remove(path: Path) -> None:
        path.unlink(missing_ok=True)
