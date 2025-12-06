from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID)->Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) ->Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass