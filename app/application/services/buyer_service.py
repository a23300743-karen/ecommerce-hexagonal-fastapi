from app.domain.models.buyer_profile import BuyerProfile
from app.domain.ports.buyer_repository import BuyerRepository


class BuyerService:

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

        if "@" not in email:
            raise ValueError("Correo invalido")

        if self.repository.get_by_email(email) is not None:
            raise ValueError("El correo ya existe")

        buyer = BuyerProfile(
            id=0,
            name=name,
            email=email,
            address=address,
            phone=phone
        )

        return self.repository.save(buyer)

    def list_buyers(self):
        return self.repository.get_all()

    def get_buyer(self, buyer_id: int) -> BuyerProfile:
        buyer = self.repository.get_by_id(buyer_id)

        if buyer is None:
            raise ValueError("El perfil de compra no existe")

        return buyer
