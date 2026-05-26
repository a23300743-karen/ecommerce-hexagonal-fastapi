from fastapi import APIRouter, HTTPException

from app.adapters.api.schemas.buyer_schema import BuyerRequest, BuyerResponse
from app.application.services.buyer_service import BuyerService

router = APIRouter(
    prefix="/buyers",
    tags=["Buyers"]
)

def get_buyer_router(
    service: BuyerService
):

    @router.post("/", response_model=BuyerResponse)
    def create_buyer(
        request: BuyerRequest
    ):

        try:

            return service.create_buyer(
                request.name,
                request.email,
                request.address,
                request.phone
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.get("/", response_model=list[BuyerResponse])
    def list_buyers():

        return service.list_buyers()

    @router.get("/{buyer_id}", response_model=BuyerResponse)
    def get_buyer(
        buyer_id: int
    ):

        try:

            return service.get_buyer(buyer_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    return router
