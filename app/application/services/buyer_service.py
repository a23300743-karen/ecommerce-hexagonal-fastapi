from app.domain.models.buyer_profile import BuyerProfile
from app.domain.ports.buyer_repository import BuyerRepository


class BuyerService:

    VALID_STATUSES = {"ACTIVE", "INACTIVE"}

    def __init__(
        self,
        repository: BuyerRepository
    ):
        self.repository = repository

    def create_buyer(
        self,
        name: str,
        email: str,
        address: str,
        phone: str | None = None
    ) -> BuyerProfile:

        self._validate_buyer_data(name, email, address, phone)

        if self.repository.get_by_email(email.strip()) is not None:
            raise ValueError("El correo ya existe")

        buyer = BuyerProfile(
            id=0,
            name=name.strip(),
            email=email.strip(),
            address=address.strip(),
            phone=phone.strip() if phone else None,
            status="ACTIVE"
        )

        return self.repository.save(buyer)

    def list_buyers(self):
        return self.repository.get_all()

    def get_buyer(self, buyer_id: int) -> BuyerProfile:
        buyer = self.repository.get_by_id(buyer_id)

        if buyer is None:
            raise ValueError("El perfil de compra no existe")

        return buyer

    def search_buyers_by_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("El nombre de busqueda no puede estar vacio")

        return self.repository.search_by_name(name.strip())

    def update_buyer(
        self,
        buyer_id: int,
        name: str,
        email: str,
        address: str,
        phone: str | None,
        status: str
    ) -> BuyerProfile:

        current_buyer = self.get_buyer(buyer_id)
        self._validate_buyer_data(name, email, address, phone, status)

        existing_buyer = self.repository.get_by_email(email.strip())

        if existing_buyer is not None and existing_buyer.id != buyer_id:
            raise ValueError("El correo ya existe")

        buyer = BuyerProfile(
            id=buyer_id,
            name=name.strip(),
            email=email.strip(),
            address=address.strip(),
            phone=phone.strip() if phone else None,
            status=status or current_buyer.status
        )

        updated_buyer = self.repository.update(buyer_id, buyer)

        if updated_buyer is None:
            raise ValueError("El perfil de compra no existe")

        return updated_buyer

    def deactivate_buyer(self, buyer_id: int) -> BuyerProfile:
        self.get_buyer(buyer_id)

        buyer = self.repository.change_status(buyer_id, "INACTIVE")

        if buyer is None:
            raise ValueError("El perfil de compra no existe")

        return buyer

    def _validate_buyer_data(
        self,
        name: str,
        email: str,
        address: str,
        phone: str | None = None,
        status: str = "ACTIVE"
    ):

        if not name or not name.strip():
            raise ValueError("El nombre del comprador no puede estar vacio")

        if not email or not email.strip():
            raise ValueError("El correo no puede estar vacio")

        clean_email = email.strip()

        if "@" not in clean_email or not clean_email.endswith(".com"):
            raise ValueError("El correo debe contener @ y terminar en .com")

        if not address or not address.strip():
            raise ValueError("La direccion no puede estar vacia")

        if phone:
            digits = "".join(character for character in phone if character.isdigit())

            if len(digits) < 10:
                raise ValueError("El telefono debe tener minimo 10 digitos")

        if status not in self.VALID_STATUSES:
            raise ValueError("El status debe ser ACTIVE o INACTIVE")
