from abc import ABC, abstractmethod


class StoragePort(ABC):
    @abstractmethod
    async def save(self, key: str, data: bytes, content_type: str) -> str:
        """Persiste o conteúdo e retorna a URL pública de acesso."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Remove o conteúdo identificado por key."""
