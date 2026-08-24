from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.asset import AssetRepository
from app.repositories.notebook import NotebookRepository
from app.repositories.page import PageRepository
from app.repositories.user import UserRepository
from app.services.asset import AssetService
from app.services.auth import AuthService
from app.services.content import ContentService
from app.services.notebook import NotebookService
from app.services.page import PageService
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
