from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.factory import get_user_repository
from app.schemas.auth import (
    LoginRequest,
    LoginResponseData,
    RefreshTokenRequest,
    TokenPair,
    UserOut,
)
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService, InvalidCredentialsError, InvalidTokenError

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service() -> AuthService:
    return AuthService(user_repository=get_user_repository())


@router.post("/login", response_model=ApiResponse[LoginResponseData])
async def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user, access_token, refresh_token = await auth_service.authenticate(
            payload.email, payload.password
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return ApiResponse(
        success=True,
        message="Login successful",
        data=LoginResponseData(
            user=UserOut.model_validate(user),
            tokens=TokenPair(access_token=access_token, refresh_token=refresh_token),
        ),
    )


@router.post("/refresh", response_model=ApiResponse[dict])
async def refresh(payload: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        new_access_token = await auth_service.refresh_access_token(payload.refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return ApiResponse(
        success=True,
        message="Token refreshed",
        data={"access_token": new_access_token},
    )


@router.get("/me", response_model=ApiResponse[UserOut])
async def get_me(current_user: User = Depends(get_current_user)):
    return ApiResponse(
        success=True,
        message="Current user retrieved",
        data=UserOut.model_validate(current_user),
    )


@router.post("/logout", response_model=ApiResponse[None])
async def logout():
    return ApiResponse(success=True, message="Logged out successfully", data=None)
