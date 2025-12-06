# src/infrastructure/repositories/product_repository.py
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
# We don't need update/insert imports if we use session.merge/add

from src.domain.entities.product import Product
from src.domain.repositories.product import IProductRepository
from src.infrastructure.schemas.product_orm import ProductORM


class SQLAlchemyProductRepository(IProductRepository):
    def __init__(self, session):
        self._session = session

    # Helper to convert ORM -> Entity
    def _to_entity(self, orm_model: ProductORM) -> Product:
        return Product(
            id=orm_model.id,
            name=orm_model.name,
            price=orm_model.price,
            stock=orm_model.stock,
        )

    # Helper to convert Entity -> ORM
    def _to_orm(self, entity: Product) -> ProductORM:
        return ProductORM(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            stock=entity.stock
        )

    async def save(self, product: Product) -> Product:
        product_orm = self._to_orm(product)
        await self._session.merge(product_orm)
        # commit will be done from uni of work
        return product

    async def list_all(self) -> List[Product]:
        stmt = select(ProductORM).order_by(ProductORM.name)
        result = await self._session.execute(stmt)
        orm_models = result.scalars().all()

        return [self._to_entity(model) for model in orm_models]

    async def get_by_id(self, id: UUID) -> Optional[Product]:
        stmt = select(ProductORM).where(ProductORM.id == id)
        result = await self._session.execute(stmt)
        orm_model = result.scalar_one_or_none()

        if orm_model is None:
            return None

        return self._to_entity(orm_model)