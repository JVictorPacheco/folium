from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

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


class NotebookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    page_mode: PageMode
    line_color: str
    line_spacing: int
    created_at: datetime
    updated_at: datetime
