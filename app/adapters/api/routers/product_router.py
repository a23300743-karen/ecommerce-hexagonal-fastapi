from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from app.adapters.api.dependencies.auth_dependencies import require_admin
from app.adapters.api.schemas.product_schema import ProductResponse
from app.application.services.product_service import ProductService
from app.infrastructure.storage.local_file_storage import LocalFileStorage

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

storage = LocalFileStorage()


def get_product_router(
    service: ProductService
):

    @router.post("/", response_model=ProductResponse)
    async def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        status: str = Form("ACTIVE"),
        image: UploadFile | None = File(None),
        current_user=Depends(require_admin)
    ):

        try:
            image_url = await _save_image_if_present(image)

            return service.create_product(
                name,
                description,
                price,
                stock,
                status,
                image_url
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
    async def update_product(
        product_id: int,
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        status: str = Form("ACTIVE"),
        image: UploadFile | None = File(None),
        current_user=Depends(require_admin)
    ):

        try:
            image_url = await _save_image_if_present(image)

            return service.update_product(
                product_id,
                name,
                description,
                price,
                stock,
                status,
                image_url
            )

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    @router.delete("/{product_id}", response_model=ProductResponse)
    def delete_product(
        product_id: int,
        current_user=Depends(require_admin)
    ):

        try:

            return service.deactivate_product(product_id)

        except ValueError as error:

            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

    return router


async def _save_image_if_present(image: UploadFile | None) -> str | None:
    if image is None or not image.filename:
        return None

    content = await image.read()

    if not content:
        return None

    return await storage.save_product_image(
        filename=image.filename,
        content=content,
        content_type=image.content_type or ""
    )
