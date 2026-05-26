from passlib.context import CryptContext

from app.domain.ports.password_service import PasswordService

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class BcryptPasswordService(PasswordService):

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)
