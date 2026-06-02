from abc import ABC, abstractmethod


class FileStorage(ABC):

    @abstractmethod
    async def save_product_image(
        self,
        filename: str,
        content: bytes,
        content_type: str
    ) -> str:
        pass
