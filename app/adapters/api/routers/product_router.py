from fastapi import APIRouter, HTTPException, Query

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
                request.stock,
                request.status
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.get("/", response_model=list[ProductResponse])
    def list_products():

        return service.list_products()

    @router.get("/search", response_model=list[ProductResponse])
    def search_products(
        name: str = Query(..., min_length=1)
    ):

        try:

            return service.search_products_by_name(name)

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

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

    @router.put("/{product_id}", response_model=ProductResponse)
    def update_product(
        product_id: int,
        request: ProductRequest
    ):

        try:

            return service.update_product(
                product_id,
                request.name,
                request.description,
                request.price,
                request.stock,
                request.status
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.delete("/{product_id}", response_model=ProductResponse)
    def delete_product(
        product_id: int
    ):

        try:

            return service.deactivate_product(product_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    return router
