from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.infrastructure.security.jwt_service import JWTService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    token_service = JWTService()

    try:
        payload = token_service.decode_access_token(token)
        user_id = int(payload.get("sub"))

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token invalido"
        )

    repository = MySQLUserRepository()
    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    if user.status != "ACTIVE":
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    return user


def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos de administrador"
        )

    return current_user
