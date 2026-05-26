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

            raise ValueError(
                "Correo inválido"
            )

        buyer = BuyerProfile(
            id=0,
            name=name,
            email=email,
            address=address,
            phone=phone
        )

        return self.repository.save(
            buyer
        )

    def list_buyers(
        self
    ):

        return self.repository.get_all()