from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.domain.enums import SharePermission


class ShareCreate(BaseModel):
    email: EmailStr
    permission: SharePermission = SharePermission.VIEWER


class ShareOut(BaseModel):
    id: int
    notebook_id: int
    email: str
    permission: SharePermission
    created_at: datetime
