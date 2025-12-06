from sqlalchemy.ext.asyncio import async_sessionmaker

from src.domain.unit_of_work import IUnitOfWork
from src.infrastructure.repositories.product_repository import SQLAlchemyProductRepository
from src.infrastructure.repositories.user_repository import SQLAlchemyUserRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory

    async def __aenter__(self):
        self._session = self._session_factory()
        self.products = SQLAlchemyProductRepository(self._session)
        self.users = SQLAlchemyUserRepository(self._session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


