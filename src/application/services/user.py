from passlib.context import CryptContext
from pydantic import EmailStr

from src.domain.entities.user import User
from src.domain.unit_of_work import IUnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def create_user(self, name: str, email: EmailStr, password: str) -> User:
        async with self._uow as uow:
            existing = await uow.users.get_by_email(email)
            if existing:
                raise ValueError("Email already registered")

            hashed_password = pwd_context.hash(password)

            user = User(name=name, email=email, password_hash=hashed_password)
            saved_user = await self._uow.users.save(user)
            return user

