from abc import ABC, abstractmethod
from app.domain.models.buyer_profile import BuyerProfile

class BuyerRepository(ABC):

    @abstractmethod
    def save(self, buyer: BuyerProfile) -> BuyerProfile:
        pass

    @abstractmethod
    def get_by_id(self, buyer_id: int) -> BuyerProfile | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> BuyerProfile | None:
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> list[BuyerProfile]:
        pass

    @abstractmethod
    def get_all(self) -> list[BuyerProfile]:
        pass

    @abstractmethod
    def update(self, buyer_id: int, buyer: BuyerProfile) -> BuyerProfile | None:
        pass

    @abstractmethod
    def change_status(self, buyer_id: int, status: str) -> BuyerProfile | None:
        pass
