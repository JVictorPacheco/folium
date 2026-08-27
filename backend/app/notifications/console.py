import logging

from app.notifications.port import EmailSender

logger = logging.getLogger("uvicorn.error")


class ConsoleEmailSender(EmailSender):
    """Escreve o link no log — substituir por adaptador SMTP quando houver envio real."""

    async def send_reset_link(self, email: str, link: str) -> None:
        logger.info("RESET DE SENHA para %s: %s", email, link)
