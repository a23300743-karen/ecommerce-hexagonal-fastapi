from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(
        self,
        name: str,
        description: str,
        price: float,
        stock: int
    ) -> Product:

        if price <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        product = Product(
            id=0,
            name=name,
            description=description,
            price=price,
            stock=stock,
            status="ACTIVE"
        )

        return self.repository.save(product)

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)

        if product is None:
            raise ValueError("El producto no existe")

        return product
