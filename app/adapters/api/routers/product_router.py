from fastapi import APIRouter, HTTPException

from app.adapters.api.schemas.product_schema import ProductRequest
from app.application.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_product_router(
    service: ProductService
):

    @router.post("/")
    def create_product(
        request: ProductRequest
    ):

        try:

            return service.create_product(
                request.name,
                request.description,
                request.price,
                request.stock
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.get("/")
    def list_products():

        return service.list_products()

    return router