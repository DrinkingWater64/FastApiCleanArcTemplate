from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.application.services.product import ProductService
from src.application.services.user import UserService
from src.core.config import settings
from src.domain.unit_of_work import IUnitOfWork
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session

def get_unit_of_work() -> IUnitOfWork:
    return SQLAlchemyUnitOfWork(session_factory)

def get_product_service(
    uow: Annotated[IUnitOfWork, Depends(get_unit_of_work)]
) -> ProductService:
    return ProductService(uow)

def get_user_service(
        uow: Annotated[IUnitOfWork, Depends(get_unit_of_work)]
) -> UserService:
    return UserService(uow)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]