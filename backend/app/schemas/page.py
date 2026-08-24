from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PageCreate(BaseModel):
    title: str = Field(default="Sem título", max_length=255)


class PageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notebook_id: int
    title: str
    position: int
    content_json: dict[str, Any]
    revision: int
    created_at: datetime
    updated_at: datetime


class PageContentUpdate(BaseModel):
    content_json: dict[str, Any]
    revision: int = Field(ge=1)


class PageContentOut(BaseModel):
    revision: int
    updated_at: datetime
