from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError

from app.adapters.api.dependencies.auth_dependencies import get_current_user
from app.adapters.api.schemas.auth_schema import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_service import BcryptPasswordService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

user_repository = MySQLUserRepository()
password_service = BcryptPasswordService()
token_service = JWTService()
auth_service = AuthService(
    user_repository,
    password_service,
    token_service
)


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest):
    try:
        user = auth_service.register(
            request.name,
            request.email,
            request.password,
            request.role
        )

        return user

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: Request):
    try:
        credentials = await _get_login_credentials(request)

        return auth_service.login(
            credentials.email,
            credentials.password
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest):
    try:
        return auth_service.refresh_access_token(
            request.refresh_token
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Refresh token invalido"
        )


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user


async def _get_login_credentials(request: Request) -> LoginRequest:
    content_type = request.headers.get("content-type", "")

    try:

        if "application/json" in content_type:
            payload = await request.json()

            return LoginRequest(
                email=payload.get("email", ""),
                password=payload.get("password", "")
            )

        form = await request.form()

        return LoginRequest(
            email=form.get("username", "") or form.get("email", ""),
            password=form.get("password", "")
        )

    except ValidationError as error:
        raise HTTPException(
            status_code=422,
            detail=error.errors()
        )
