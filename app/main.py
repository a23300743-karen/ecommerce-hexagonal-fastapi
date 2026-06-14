import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.infrastructure.repositories.mysql_product_repository import MySQLProductRepository
from app.infrastructure.repositories.mysql_buyer_repository import MySQLBuyerRepository
from app.infrastructure.repositories.mysql_order_repository import MySQLOrderRepository
from app.infrastructure.db.connection import get_connection

from app.application.services.product_service import ProductService
from app.application.services.buyer_service import BuyerService
from app.application.services.order_service import OrderService

from app.adapters.api.routers.product_router import get_product_router
from app.adapters.api.routers.buyer_router import get_buyer_router
from app.adapters.api.routers.order_router import get_order_router
from app.adapters.api.routers.auth_router import router as auth_router
from app.adapters.websocket.chat_socket import router as chat_router, support_chat_service
from app.adapters.api.routers.support_router import get_support_router


DEPLOYMENT_COLOR = os.getenv("DEPLOYMENT_COLOR", "LOCAL")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0-local")
RELEASE_MESSAGE = os.getenv("RELEASE_MESSAGE", "Desarrollo local")
FEATURE_CHECKOUT_CONFIRMATION = os.getenv(
    "FEATURE_CHECKOUT_CONFIRMATION", "true"
).lower() == "true"
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="E-commerce de tecnologia",
    description="Backend de e-commerce usando FastAPI y Arquitectura Hexagonal",
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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

app.include_router(auth_router)
app.include_router(get_product_router(product_service))
app.include_router(get_buyer_router(buyer_service))
app.include_router(get_order_router(order_service))
app.include_router(get_support_router(support_chat_service))
app.include_router(chat_router)

@app.get("/deployment", include_in_schema=False)
def deployment_info():
    return {
        "environment": DEPLOYMENT_COLOR,
        "version": APP_VERSION,
        "message": RELEASE_MESSAGE,
        "features": {
            "checkout_confirmation": FEATURE_CHECKOUT_CONFIRMATION
        }
    }


@app.get("/health", include_in_schema=False)
def health_check():
    if os.getenv("FORCE_UNHEALTHY", "false").lower() == "true":
        raise HTTPException(
            status_code=503,
            detail="Fallo simulado para demostrar una promocion rechazada"
        )

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="La aplicacion no puede conectarse a MySQL"
        ) from error

    return {
        "status": "healthy",
        "environment": DEPLOYMENT_COLOR,
        "version": APP_VERSION,
        "database": "connected"
    }


if FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend"
    )
