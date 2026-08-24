from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset


class AssetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: int, **values) -> Asset:
        asset = Asset(user_id=user_id, **values)
        self._session.add(asset)
        await self._session.commit()
        await self._session.refresh(asset)
        return asset
