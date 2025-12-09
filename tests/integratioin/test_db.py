import pytest
from sqlalchemy import text
from src.presentation.dependencies import get_db_session

@pytest.mark.asyncio
async def test_database_connection():
    async for session in get_db_session():
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
