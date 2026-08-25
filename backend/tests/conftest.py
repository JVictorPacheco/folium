import pytest
from fastapi import Depends
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api.deps import get_asset_service
from app.core.database import Base, get_db
from app.main import app
from app.repositories.asset import AssetRepository
from app.services.asset import AssetService
from app.storage.local import LocalStorage


@pytest.fixture
async def client(tmp_path):
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    storage = LocalStorage(str(tmp_path / "media"))

    async def override_get_asset_service(db: AsyncSession = Depends(get_db)):
        return AssetService(AssetRepository(db), storage)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_asset_service] = override_get_asset_service
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


async def register(client: AsyncClient, email: str = "user@example.com", password: str = "senha1234") -> str:
    resp = await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 201, resp.text
    return resp.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
