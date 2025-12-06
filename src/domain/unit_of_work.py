from abc import ABC, abstractmethod

from src.domain.repositories.product import IProductRepository
from src.domain.repositories.user import IUserRepository


class IUnitOfWork(ABC):
    products: IProductRepository
    users: IUserRepository

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
