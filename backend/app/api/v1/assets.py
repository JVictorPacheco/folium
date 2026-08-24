from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.api.deps import get_asset_service
from app.core.config import settings
from app.core.deps import get_current_user
from app.domain.enums import AssetKind
from app.models.user import User
from app.schemas.asset import AssetOut
from app.services.asset import AssetService

router = APIRouter(prefix="/assets", tags=["assets"])

IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp", "image/gif"}


@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    file: UploadFile = File(...),
    kind: AssetKind = Form(...),
    user: User = Depends(get_current_user),
    service: AssetService = Depends(get_asset_service),
) -> AssetOut:
    data = await file.read()
    mime = file.content_type or "application/octet-stream"

    if kind is AssetKind.IMAGE:
        if mime not in IMAGE_MIMES or len(data) > settings.max_image_bytes:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Imagem inválida (tipo ou tamanho)")
    elif kind is AssetKind.PDF:
        if mime != "application/pdf" or len(data) > settings.max_pdf_bytes:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "PDF inválido (tipo ou tamanho)")

    return await service.upload(user.id, kind, file.filename or "arquivo", mime, data)
