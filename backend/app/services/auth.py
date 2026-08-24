from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        email = email.strip().lower()
        existing = await self._user_repo.get_by_email(email)
        if existing is not None:
            raise AuthError("E-mail já cadastrado")
        return await self._user_repo.create(email, hash_password(password))

    async def authenticate(self, email: str, password: str) -> User:
        email = email.strip().lower()
        user = await self._user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthError("Credenciais inválidas")
        return user

    @staticmethod
    def create_token(user: User) -> str:
        return create_access_token(str(user.id))
