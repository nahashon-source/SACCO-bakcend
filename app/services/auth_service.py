"""
Auth business logic. Routes call this service; the service calls the
repository. Routes must never talk to repositories directly.
"""

from jose import JWTError

from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password
from app.models.user import User
from app.repositories.mock.user_repository import MockUserRepository


class InvalidCredentialsError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: MockUserRepository):
        self._user_repository = user_repository

    async def authenticate(self, email: str, password: str) -> tuple[User, str, str]:
        user = await self._user_repository.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password")

        if not user.is_active:
            raise InvalidCredentialsError("This account has been deactivated")

        access_token = create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})
        refresh_token = create_refresh_token(subject=str(user.id))

        return user, access_token, refresh_token

    async def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = decode_token(refresh_token)
        except JWTError as exc:
            raise InvalidTokenError(str(exc)) from exc

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Provided token is not a refresh token")

        user_id = int(payload["sub"])
        user = await self._user_repository.get_by_id(user_id)

        if user is None or not user.is_active:
            raise InvalidTokenError("User no longer exists or is inactive")

        return create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})

    async def get_current_user_from_token(self, access_token: str) -> User:
        try:
            payload = decode_token(access_token)
        except JWTError as exc:
            raise InvalidTokenError(str(exc)) from exc

        if payload.get("type") != "access":
            raise InvalidTokenError("Provided token is not an access token")

        user = await self._user_repository.get_by_id(int(payload["sub"]))
        if user is None:
            raise InvalidTokenError("User no longer exists")

        return user
