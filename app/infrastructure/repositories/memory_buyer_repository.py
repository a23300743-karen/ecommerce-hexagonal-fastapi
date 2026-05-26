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

    def get_all(self):
        return self.buyers
