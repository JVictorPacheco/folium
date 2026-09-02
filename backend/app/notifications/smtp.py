import asyncio
import smtplib
from email.message import EmailMessage

from app.notifications.port import EmailSender


class SmtpEmailSender(EmailSender):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        from_email: str,
        use_tls: bool = True,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._from_email = from_email
        self._use_tls = use_tls

    async def send_reset_link(self, email: str, link: str) -> None:
        await asyncio.to_thread(self._send, email, link)

    def _send(self, email: str, link: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Recuperação de senha — Folium"
        msg["From"] = self._from_email
        msg["To"] = email
        msg.set_content(
            "Olá!\n\n"
            "Você solicitou a recuperação de senha no Folium.\n"
            "Use o link abaixo para definir uma nova senha (válido por 1 hora):\n\n"
            f"{link}\n\n"
            "Se você não pediu isso, ignore este e-mail.\n"
        )

        with smtplib.SMTP(self._host, self._port, timeout=10) as server:
            if self._use_tls:
                server.starttls()
            if self._username:
                server.login(self._username, self._password)
            server.send_message(msg)
