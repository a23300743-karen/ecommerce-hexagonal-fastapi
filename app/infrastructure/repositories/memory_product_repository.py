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

    def search_by_name(self, name: str):
        clean_name = name.lower()

        return [
            product
            for product in self.products
            if clean_name in product.name.lower()
        ]

    def update(self, product_id: int, product: Product):
        current_product = self.get_by_id(product_id)

        if current_product is None:
            return None

        current_product.name = product.name
        current_product.description = product.description
        current_product.price = product.price
        current_product.stock = product.stock
        current_product.status = product.status
        current_product.image_url = product.image_url

        return current_product

    def update_stock(self, product_id: int, stock: int):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        product.stock = stock
        return product

    def change_status(self, product_id: int, status: str):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        product.status = status
        return product
