from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select

from src.domain.entities.user import User
from src.domain.repositories.user import IUserRepository
from src.infrastructure.schemas.user_orm import UserOrm


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session):
        self._session = session

    async def get_by_id(self, id: UUID) -> Optional[User]:
        stmt = select(UserOrm).where(UserOrm.id == id)
        result = self._session.execute(stmt)
        orm_model = result.scalar_one_or_none()

        if orm_model is None:
            return None

        return self._to_entity(orm_model)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserOrm).where(UserOrm.email == email)
        result =self._session.execute(stmt)
        user_orm = result.scalar_one_or_none()
        return self._to_entity(user_orm) if user_orm else None

    async def save(self, user: User) -> User:
        user_orm = self._to_orm(user)
        self._session.merge(user_orm)
        # commit from unit of work
        return user


    def _to_entity(self, orm: UserOrm) -> User:
        return User.model_validate(orm, from_attributes=True)

    def _to_orm(self, user: User) -> UserOrm:
        return UserOrm(
            id=user.id,
            name=user.name,
            email=str(user.email),
            password_hash=user.password_hash,
            is_active=user.is_active,
        )


