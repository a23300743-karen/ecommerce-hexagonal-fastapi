from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository


class ProductService:

    VALID_STATUSES = {"ACTIVE", "INACTIVE"}

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(
        self,
        name: str,
        description: str,
        price: float,
        stock: int,
        status: str = "ACTIVE"
    ) -> Product:

        self._validate_product_data(name, description, price, stock, status)

        product = Product(
            id=0,
            name=name.strip(),
            description=description.strip(),
            price=price,
            stock=stock,
            status=status
        )

        return self.repository.save(product)

    def list_products(self):
        return self.repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)

        if product is None:
            raise ValueError("El producto no existe")

        return product

    def search_products_by_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("El nombre de busqueda no puede estar vacio")

        return self.repository.search_by_name(name.strip())

    def update_product(
        self,
        product_id: int,
        name: str,
        description: str,
        price: float,
        stock: int,
        status: str
    ) -> Product:

        self.get_product(product_id)
        self._validate_product_data(name, description, price, stock, status)

        product = Product(
            id=product_id,
            name=name.strip(),
            description=description.strip(),
            price=price,
            stock=stock,
            status=status
        )

        updated_product = self.repository.update(product_id, product)

        if updated_product is None:
            raise ValueError("El producto no existe")

        return updated_product

    def deactivate_product(self, product_id: int) -> Product:
        self.get_product(product_id)

        product = self.repository.change_status(product_id, "INACTIVE")

        if product is None:
            raise ValueError("El producto no existe")

        return product

    def _validate_product_data(
        self,
        name: str,
        description: str,
        price: float,
        stock: int,
        status: str
    ):

        if not name or not name.strip():
            raise ValueError("El nombre del producto no puede estar vacio")

        if not description or not description.strip():
            raise ValueError("La descripcion del producto no puede estar vacia")

        if price <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        if status not in self.VALID_STATUSES:
            raise ValueError("El status debe ser ACTIVE o INACTIVE")
