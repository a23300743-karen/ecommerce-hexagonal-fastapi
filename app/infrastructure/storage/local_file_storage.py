import os
from pathlib import Path
from uuid import uuid4

from app.domain.ports.file_storage import FileStorage

UPLOAD_ROOT = Path("uploads/products")
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}


class LocalFileStorage(FileStorage):

    async def save_product_image(
        self,
        filename: str,
        content: bytes,
        content_type: str
    ) -> str:

        if content_type not in ALLOWED_IMAGE_TYPES:
            raise ValueError("La imagen debe ser JPG, PNG o WEBP")

        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

        extension = Path(filename).suffix.lower() or ".jpg"
        safe_name = f"{uuid4()}{extension}"
        path = UPLOAD_ROOT / safe_name

        with open(path, "wb") as image_file:
            image_file.write(content)

        return f"/uploads/products/{safe_name}"
