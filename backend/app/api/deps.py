from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.notifications.console import ConsoleEmailSender
from app.notifications.port import EmailSender
from app.notifications.smtp import SmtpEmailSender
from app.repositories.asset import AssetRepository
from app.repositories.notebook import NotebookRepository
from app.repositories.page import PageRepository
from app.repositories.password_reset import PasswordResetRepository
from app.repositories.user import UserRepository
from app.services.asset import AssetService
from app.services.auth import AuthService
from app.services.content import ContentService
from app.services.notebook import NotebookService
from app.services.page import PageService
from app.services.password_reset import PasswordResetService
from app.storage.local import LocalStorage


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_notebook_service(db: AsyncSession = Depends(get_db)) -> NotebookService:
    return NotebookService(NotebookRepository(db))


def get_page_service(db: AsyncSession = Depends(get_db)) -> PageService:
    return PageService(PageRepository(db), NotebookRepository(db))


def get_content_service(db: AsyncSession = Depends(get_db)) -> ContentService:
    return ContentService(PageRepository(db))


def get_asset_service(db: AsyncSession = Depends(get_db)) -> AssetService:
    return AssetService(AssetRepository(db), LocalStorage())


def get_email_sender() -> EmailSender:
    if settings.smtp_host:
        return SmtpEmailSender(
            settings.smtp_host,
            settings.smtp_port,
            settings.smtp_username,
            settings.smtp_password,
            settings.smtp_from_email,
            settings.smtp_use_tls,
        )
    return ConsoleEmailSender()


def get_password_reset_service(
    db: AsyncSession = Depends(get_db),
    sender: EmailSender = Depends(get_email_sender),
) -> PasswordResetService:
    return PasswordResetService(
        UserRepository(db),
        PasswordResetRepository(db),
        sender,
        settings.frontend_url,
    )
