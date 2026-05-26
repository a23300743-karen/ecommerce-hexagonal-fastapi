from abc import ABC, abstractmethod
from app.domain.models.product import Product

class ProductRepository(ABC):

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_all(self) -> list[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product | None:
        pass