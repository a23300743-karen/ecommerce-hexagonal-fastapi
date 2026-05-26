from fastapi import APIRouter, HTTPException

from app.adapters.api.schemas.order_schema import OrderRequest
from app.application.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_order_router(
    service: OrderService
):

    @router.post("/")
    def create_order(
        request: OrderRequest
    ):

        try:

            return service.create_order(
                request.buyer_id,
                request.product_id,
                request.quantity
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.get("/")
    def list_orders():

        return service.list_orders()

    @router.patch("/{order_id}/cancel")
    def cancel_order(
        order_id: int
    ):

        try:

            return service.cancel_order(
                order_id
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    return router