from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth import AuthError, AuthService

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
