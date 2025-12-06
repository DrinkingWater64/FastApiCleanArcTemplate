from decimal import Decimal
from uuid import UUID

from sqlalchemy import Uuid, String, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.schemas.base_orm import Base
from src.infrastructure.schemas.mixin import TimestampMixin


class ProductORM(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)