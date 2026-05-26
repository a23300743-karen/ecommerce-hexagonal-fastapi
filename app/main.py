from fastapi import FastAPI

from app.infrastructure.repositories.mysql_product_repository import MySQLProductRepository
from app.infrastructure.repositories.mysql_buyer_repository import MySQLBuyerRepository
from app.infrastructure.repositories.mysql_order_repository import MySQLOrderRepository

from app.application.services.product_service import ProductService
from app.application.services.buyer_service import BuyerService
from app.application.services.order_service import OrderService

from app.adapters.api.routers.product_router import get_product_router
from app.adapters.api.routers.buyer_router import get_buyer_router
from app.adapters.api.routers.order_router import get_order_router

app = FastAPI(
    title="E-commerce mini Amazon tecnología",
    description="Backend de e-commerce usando FastAPI y Arquitectura Hexagonal",
    version="1.0.0"
)

product_repository = MySQLProductRepository()
buyer_repository = MySQLBuyerRepository()
order_repository = MySQLOrderRepository()

product_service = ProductService(product_repository)
buyer_service = BuyerService(buyer_repository)

order_service = OrderService(
    order_repository,
    product_repository,
    buyer_repository
)

app.include_router(get_product_router(product_service))
app.include_router(get_buyer_router(buyer_service))
app.include_router(get_order_router(order_service))