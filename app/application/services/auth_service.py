from app.domain.models.buyer_profile import BuyerProfile
from app.domain.models.user import User
from app.domain.ports.buyer_repository import BuyerRepository
from app.domain.ports.password_service import PasswordService
from app.domain.ports.token_service import TokenService
from app.domain.ports.user_repository import UserRepository


class AuthService:

    VALID_ROLES = {"ADMIN", "CUSTOMER"}

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
        buyer_repository: BuyerRepository | None = None
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.token_service = token_service
        self.buyer_repository = buyer_repository

    def register(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "CUSTOMER",
        address: str | None = None,
        phone: str | None = None
    ) -> User:

        self._validate_register_data(name, email, password, role, address, phone)

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

        saved_user = self.user_repository.save(user)

        if role == "CUSTOMER" and self.buyer_repository is not None:
            existing_buyer = self.buyer_repository.get_by_email(clean_email)

            if existing_buyer is None:
                buyer = BuyerProfile(
                    id=0,
                    name=saved_user.name,
                    email=saved_user.email,
                    address=address.strip(),
                    phone=phone.strip() if phone else None,
                    status="ACTIVE",
                    user_id=saved_user.id
                )
                self.buyer_repository.save(buyer)

        return saved_user

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email.strip())

        if user is None:
            raise ValueError("Credenciales invalidas")

        if user.status != "ACTIVE":
            raise ValueError("Usuario inactivo")

        if not self.password_service.verify_password(password, user.password_hash):
            raise ValueError("Credenciales invalidas")

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }

        access_token = self.token_service.create_access_token(token_data)
        refresh_token = self.token_service.create_refresh_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str):
        payload = self.token_service.decode_refresh_token(refresh_token)

        user_id = int(payload.get("sub"))
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise ValueError("Usuario no encontrado")

        if user.status != "ACTIVE":
            raise ValueError("Usuario inactivo")

        access_token = self.token_service.create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def _validate_register_data(
        self,
        name: str,
        email: str,
        password: str,
        role: str,
        address: str | None,
        phone: str | None
    ):

        if not name or not name.strip():
            raise ValueError("El nombre es obligatorio")

        if not email or "@" not in email or not email.strip().endswith(".com"):
            raise ValueError("Correo invalido")

        if len(password) < 6:
            raise ValueError("La contrasena debe tener minimo 6 caracteres")

        if role not in self.VALID_ROLES:
            raise ValueError("El role debe ser ADMIN o CUSTOMER")

        if role == "CUSTOMER":
            if not address or not address.strip():
                raise ValueError("La direccion es obligatoria para clientes")

            if phone:
                digits = "".join(character for character in phone if character.isdigit())
                if len(digits) < 10:
                    raise ValueError("El telefono debe tener minimo 10 digitos")
