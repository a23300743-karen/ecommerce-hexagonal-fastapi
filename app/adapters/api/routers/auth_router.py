from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.adapters.api.dependencies.auth_dependencies import get_current_user
from app.adapters.api.schemas.auth_schema import (
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse
)
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.mysql_buyer_repository import MySQLBuyerRepository
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_service import BcryptPasswordService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

user_repository = MySQLUserRepository()
buyer_repository = MySQLBuyerRepository()
password_service = BcryptPasswordService()
token_service = JWTService()
auth_service = AuthService(
    user_repository,
    password_service,
    token_service,
    buyer_repository
)


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest):
    try:
        user = auth_service.register(
            request.name,
            request.email,
            request.password,
            "CUSTOMER",
            request.address,
            request.phone
        )

        return user

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return auth_service.login(
            form_data.username,
            form_data.password
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
