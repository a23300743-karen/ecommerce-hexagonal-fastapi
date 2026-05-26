from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository


class MemoryProductRepository(ProductRepository):

    def __init__(self):
        self.products = []
        self.current_id = 1

    def save(self, product: Product) -> Product:
        product.id = self.current_id
        self.current_id += 1
        self.products.append(product)
        return product

    def get_all(self):
        return self.products

    def get_by_id(self, product_id: int):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def update_stock(self, product_id: int, stock: int):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        product.stock = stock
        return product
