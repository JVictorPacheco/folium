from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import generate_reset_token, hash_password, hash_reset_token
from app.notifications.port import EmailSender
from app.repositories.password_reset import PasswordResetRepository
from app.repositories.user import UserRepository


class ResetError(Exception):
    pass


class PasswordResetService:
    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: PasswordResetRepository,
        email_sender: EmailSender,
        frontend_url: str,
    ) -> None:
        self._user_repo = user_repo
        self._token_repo = token_repo
        self._email_sender = email_sender
        self._frontend_url = frontend_url

    async def request_reset(self, email: str) -> None:
        user = await self._user_repo.get_by_email(email.strip().lower())
        if user is None:
            return

        token = generate_reset_token()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.reset_token_expire_minutes)
        await self._token_repo.create(user.id, hash_reset_token(token), expires_at)

        link = f"{self._frontend_url}/reset-password?token={token}"
        await self._email_sender.send_reset_link(email, link)

    async def reset(self, token: str, new_password: str) -> None:
        record = await self._token_repo.get_valid(hash_reset_token(token))
        if record is None:
            raise ResetError("Token inválido ou expirado")

        await self._user_repo.update_password(record.user_id, hash_password(new_password))
        await self._token_repo.mark_used(record.id)
