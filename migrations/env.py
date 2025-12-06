import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from sqlalchemy.engine import Connection
from alembic import context

# --- CUSTOM CONFIG ---
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from src.core.config import settings
from src.infrastructure.schemas.base_orm import Base
from src.infrastructure.schemas.product_orm import ProductORM  # ensure models are imported
from src.infrastructure.schemas.user_orm import UserOrm

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("asyncpg", "psycopg2"))
# --- END CUSTOM CONFIG ---

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a synchronous engine (psycopg2)."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
