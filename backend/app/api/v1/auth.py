from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_password_reset_service
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.services.auth import AuthError, AuthService
from app.services.password_reset import PasswordResetService, ResetError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    try:
        user = await service.register(body.email, body.password)
    except AuthError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return TokenResponse(access_token=service.create_token(user))


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        user = await service.authenticate(body.email, body.password)
    except AuthError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc
    return TokenResponse(access_token=service.create_token(user))


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    body: ForgotPasswordRequest,
    service: PasswordResetService = Depends(get_password_reset_service),
) -> MessageResponse:
    await service.request_reset(body.email)
    return MessageResponse(message="Se o e-mail existir, enviaremos um link de recuperação")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    body: ResetPasswordRequest,
    service: PasswordResetService = Depends(get_password_reset_service),
) -> MessageResponse:
    try:
        await service.reset(body.token, body.new_password)
    except ResetError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return MessageResponse(message="Senha atualizada com sucesso")
