from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.enums import PageMode


class NotebookCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    page_mode: PageMode = PageMode.CONTINUOUS
    line_color: str = "#D9CDB4"
    line_spacing: int = Field(default=28, ge=16, le=64)


class NotebookUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    page_mode: PageMode | None = None
    line_color: str | None = None
    line_spacing: int | None = Field(default=None, ge=16, le=64)
    tags: list[str] | None = None


class NotebookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    page_mode: PageMode
    line_color: str
    line_spacing: int
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def _tag_names(cls, value: Any) -> Any:
        if not value:
            return value
        names = [tag.name for tag in value] if not isinstance(value[0], str) else value
        return sorted(names)
