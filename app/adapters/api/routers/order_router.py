from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.dependencies.auth_dependencies import get_current_user
from app.adapters.api.schemas.order_schema import OrderItemResponse, OrderRequest, OrderResponse
from app.application.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_order_router(
    service: OrderService
):

    @router.post("/", response_model=OrderResponse)
    def create_order(
        request: OrderRequest,
        current_user=Depends(get_current_user)
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

    @router.get("/", response_model=list[OrderResponse])
    def list_orders():

        return service.list_orders()

    @router.get("/{order_id}", response_model=OrderResponse)
    def get_order(
        order_id: int
    ):

        try:

            return service.get_order(order_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    @router.get("/{order_id}/items", response_model=list[OrderItemResponse])
    def get_order_items(
        order_id: int
    ):

        try:

            return service.get_order_items(order_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    @router.patch("/{order_id}/cancel", response_model=OrderResponse)
    def cancel_order(
        order_id: int,
        current_user=Depends(get_current_user)
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
