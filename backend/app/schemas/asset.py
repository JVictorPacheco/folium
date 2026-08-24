from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import AssetKind


class AssetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: AssetKind
    filename: str
    mime: str
    size: int
    url: str
    created_at: datetime
