from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    async def send_reset_link(self, email: str, link: str) -> None:
        """Envia o link de reset de senha para o e-mail do usuário."""
