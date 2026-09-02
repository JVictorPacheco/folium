from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_password_reset_service
from app.core.database import get_db
from app.main import app
from app.notifications.port import EmailSender
from app.repositories.password_reset import PasswordResetRepository
from app.repositories.user import UserRepository
from app.services.password_reset import PasswordResetService
from tests.conftest import register


class CapturingEmailSender(EmailSender):
    def __init__(self) -> None:
        self.sent: list[str] = []

    async def send_reset_link(self, email: str, link: str) -> None:
        self.sent.append(link)


def _install_override(sender: EmailSender) -> None:
    async def override(db: AsyncSession = Depends(get_db)):
        return PasswordResetService(
            UserRepository(db), PasswordResetRepository(db), sender, "http://localhost:5173"
        )

    app.dependency_overrides[get_password_reset_service] = override


def _token_from_link(link: str) -> str:
    return link.split("token=", 1)[1]


async def test_forgot_password_and_reset(client: AsyncClient) -> None:
    sender = CapturingEmailSender()
    _install_override(sender)
    await register(client, email="reset@example.com")

    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "reset@example.com"})
    assert resp.status_code == 200
    assert len(sender.sent) == 1

    token = _token_from_link(sender.sent[0])

    resp = await client.post(
        "/api/v1/auth/reset-password", json={"token": token, "new_password": "novaSenha123"}
    )
    assert resp.status_code == 200

    ok = await client.post(
        "/api/v1/auth/login", json={"email": "reset@example.com", "password": "novaSenha123"}
    )
    assert ok.status_code == 200

    old = await client.post(
        "/api/v1/auth/login", json={"email": "reset@example.com", "password": "senha1234"}
    )
    assert old.status_code == 401


async def test_forgot_password_unknown_email_returns_200(client: AsyncClient) -> None:
    sender = CapturingEmailSender()
    _install_override(sender)

    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "naoexiste@example.com"})
    assert resp.status_code == 200
    assert sender.sent == []


async def test_reset_with_invalid_token(client: AsyncClient) -> None:
    sender = CapturingEmailSender()
    _install_override(sender)
    await register(client)

    resp = await client.post(
        "/api/v1/auth/reset-password", json={"token": "token-invalido", "new_password": "novaSenha123"}
    )
    assert resp.status_code == 400


async def test_reset_token_cannot_be_reused(client: AsyncClient) -> None:
    sender = CapturingEmailSender()
    _install_override(sender)
    await register(client, email="reuse@example.com")

    await client.post("/api/v1/auth/forgot-password", json={"email": "reuse@example.com"})
    token = _token_from_link(sender.sent[0])

    first = await client.post(
        "/api/v1/auth/reset-password", json={"token": token, "new_password": "novaSenha123"}
    )
    assert first.status_code == 200

    second = await client.post(
        "/api/v1/auth/reset-password", json={"token": token, "new_password": "outraSenha123"}
    )
    assert second.status_code == 400
