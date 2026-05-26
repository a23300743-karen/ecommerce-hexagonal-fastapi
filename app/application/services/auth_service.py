from app.domain.models.user import User
from app.domain.ports.password_service import PasswordService
from app.domain.ports.token_service import TokenService
from app.domain.ports.user_repository import UserRepository


class AuthService:

    VALID_ROLES = {"ADMIN", "CUSTOMER"}

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.token_service = token_service

    def register(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "CUSTOMER"
    ) -> User:

        self._validate_register_data(name, email, password, role)

        clean_email = email.strip()

        existing_user = self.user_repository.get_by_email(clean_email)

        if existing_user is not None:
            raise ValueError("El correo ya esta registrado")

        user = User(
            id=0,
            name=name.strip(),
            email=clean_email,
            password_hash=self.password_service.hash_password(password),
            role=role,
            status="ACTIVE"
        )

        return self.user_repository.save(user)

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email.strip())

        if user is None:
            raise ValueError("Credenciales invalidas")

        if user.status != "ACTIVE":
            raise ValueError("Usuario inactivo")

        if not self.password_service.verify_password(password, user.password_hash):
            raise ValueError("Credenciales invalidas")

        token = self.token_service.create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def _validate_register_data(
        self,
        name: str,
        email: str,
        password: str,
        role: str
    ):

        if not name or not name.strip():
            raise ValueError("El nombre es obligatorio")

        if not email or "@" not in email or not email.strip().endswith(".com"):
            raise ValueError("Correo invalido")

        if len(password) < 6:
            raise ValueError("La contrasena debe tener minimo 6 caracteres")

        if role not in self.VALID_ROLES:
            raise ValueError("El role debe ser ADMIN o CUSTOMER")
