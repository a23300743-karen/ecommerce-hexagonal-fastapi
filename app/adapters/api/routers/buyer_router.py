from fastapi import APIRouter, HTTPException
import mysql.connector

from app.adapters.api.schemas.buyer_schema import BuyerRequest
from app.application.services.buyer_service import BuyerService

router = APIRouter(
    prefix="/buyers",
    tags=["Buyers"]
)

def get_buyer_router(
    service: BuyerService
):

    @router.post("/")
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

        except mysql.connector.errors.IntegrityError:

            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    @router.get("/")
    def list_buyers():

        return service.list_buyers()

    return router