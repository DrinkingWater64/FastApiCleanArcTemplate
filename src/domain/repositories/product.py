from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    async def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def list_all(self) -> List[Product]:
        pass