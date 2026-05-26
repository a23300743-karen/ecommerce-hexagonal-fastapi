from fastapi import APIRouter, HTTPException

from app.adapters.api.schemas.product_schema import ProductRequest, ProductResponse
from app.application.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_product_router(
    service: ProductService
):

    @router.post("/", response_model=ProductResponse)
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

    @router.get("/", response_model=list[ProductResponse])
    def list_products():

        return service.list_products()

    @router.get("/{product_id}", response_model=ProductResponse)
    def get_product(
        product_id: int
    ):

        try:

            return service.get_product(product_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    return router
