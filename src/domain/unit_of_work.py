from abc import ABC, abstractmethod

from src.domain.repositories.product import IProductRepository


class IUnitOfWork(ABC):
    products: IProductRepository

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
