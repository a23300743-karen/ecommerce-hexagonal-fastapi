import os
from datetime import datetime, timedelta, timezone

import jwt

from app.domain.ports.token_service import TokenService

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CAMBIA_ESTA_CLAVE_SECRETA")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)


class JWTService(TokenService):

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update(
            {
                "exp": expire,
                "token_type": "access"
            }
        )

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )

        to_encode.update(
            {
                "exp": expire,
                "token_type": "refresh"
            }
        )

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def decode_access_token(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("token_type") != "access":
            raise jwt.InvalidTokenError("Invalid access token")

        return payload

    def decode_refresh_token(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("token_type") != "refresh":
            raise jwt.InvalidTokenError("Invalid refresh token")

        return payload
