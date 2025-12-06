from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    password_hash: str
    is_active: bool = True
    # we include them as optional because these do not exist  untile we save them in db
    created_at: Optional[datetime] = None
    last_modified_at: Optional[datetime] = None

    model_config = {"from_attributes": True}