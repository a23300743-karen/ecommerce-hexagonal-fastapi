from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.dependencies.auth_dependencies import get_current_user, require_admin
from app.adapters.api.schemas.order_schema import CheckoutRequest, OrderItemResponse, OrderResponse
from app.application.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_router(service: OrderService):

    @router.post("/", response_model=OrderResponse)
    def checkout(
        request: CheckoutRequest,
        current_user=Depends(get_current_user)
    ):
        try:
            items = [item.model_dump() for item in request.items]
            return service.checkout(current_user.id, items)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))

    @router.get("/me", response_model=list[OrderResponse])
    def list_my_orders(current_user=Depends(get_current_user)):
        try:
            return service.list_orders_for_user(current_user.id)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))

    @router.get("/me/{order_id}/items", response_model=list[OrderItemResponse])
    def get_my_order_items(
        order_id: int,
        current_user=Depends(get_current_user)
    ):
        try:
            service.get_order_for_user(current_user.id, order_id)
            return service.get_order_items(order_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))

    @router.get("/", response_model=list[OrderResponse])
    def list_orders(current_user=Depends(require_admin)):
        return service.list_orders()

    @router.get("/{order_id}", response_model=OrderResponse)
    def get_order(order_id: int, current_user=Depends(require_admin)):
        try:
            return service.get_order(order_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))

    @router.get("/{order_id}/items", response_model=list[OrderItemResponse])
    def get_order_items(order_id: int, current_user=Depends(require_admin)):
        try:
            return service.get_order_items(order_id)
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))

    @router.patch("/{order_id}/cancel", response_model=OrderResponse)
    def cancel_order(
        order_id: int,
        current_user=Depends(get_current_user)
    ):
        try:
            if current_user.role != "ADMIN":
                service.get_order_for_user(current_user.id, order_id)
            return service.cancel_order(order_id)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))

    return router
