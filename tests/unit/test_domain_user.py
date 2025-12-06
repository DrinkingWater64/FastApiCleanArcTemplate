import pytest
from datetime import datetime
from uuid import UUID

from src.domain.entities.user import User


def test_user_creation_default_values():
    """Verify that a new User entity gets default values correctly."""

    # We only pass required fields (email and a placeholder hashed password)
    user = User(
        name="fake",
        email= "tests@example.com",
        password_hash="fake_hashed_pw"
    )

    # Check default values
    assert user.is_active is True
    # The ID should be auto-generated
    assert isinstance(user.id, UUID)

    # Created/Modified dates should be None before being saved by the repo
    assert user.created_at is None
    assert user.last_modified_at is None


def test_user_entity_with_audit_fields():
    """Verify the entity can hold the timestamps retrieved from the database."""

    now = datetime.now()
    # When retrieving from the DB, the Repository maps the timestamps onto the Entity
    user = User(
        name="fake",
        email="audited@example.com",
        password_hash="some_hash",
        created_at=now,
        last_modified_at=now
    )

    assert user.email == "audited@example.com"
    assert user.created_at == now
    assert user.last_modified_at == now