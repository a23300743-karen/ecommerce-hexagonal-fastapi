from app.domain.models.buyer_profile import BuyerProfile
from app.domain.ports.buyer_repository import BuyerRepository


class MemoryBuyerRepository(BuyerRepository):

    def __init__(self):
        self.buyers = []
        self.current_id = 1

    def save(self, buyer: BuyerProfile) -> BuyerProfile:
        buyer.id = self.current_id
        self.current_id += 1
        self.buyers.append(buyer)
        return buyer

    def get_by_id(self, buyer_id: int):
        for buyer in self.buyers:
            if buyer.id == buyer_id:
                return buyer
        return None

    def get_by_email(self, email: str):
        for buyer in self.buyers:
            if buyer.email == email:
                return buyer
        return None

    def get_by_user_id(self, user_id: int):
        for buyer in self.buyers:
            if buyer.user_id == user_id:
                return buyer
        return None

    def search_by_name(self, name: str):
        clean_name = name.lower()
        return [buyer for buyer in self.buyers if clean_name in buyer.name.lower()]

    def get_all(self):
        return self.buyers

    def update(self, buyer_id: int, buyer: BuyerProfile):
        current_buyer = self.get_by_id(buyer_id)
        if current_buyer is None:
            return None
        current_buyer.name = buyer.name
        current_buyer.email = buyer.email
        current_buyer.address = buyer.address
        current_buyer.phone = buyer.phone
        current_buyer.status = buyer.status
        current_buyer.user_id = buyer.user_id
        return current_buyer

    def change_status(self, buyer_id: int, status: str):
        buyer = self.get_by_id(buyer_id)
        if buyer is None:
            return None
        buyer.status = status
        return buyer
