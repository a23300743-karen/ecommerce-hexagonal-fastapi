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

    @abstractmethod
    def search_by_name(self, name: str) -> list[Product]:
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product) -> Product | None:
        pass

    @abstractmethod
    def update_stock(self, product_id: int, stock: int) -> Product | None:
        pass

    @abstractmethod
    def change_status(self, product_id: int, status: str) -> Product | None:
        pass
