import asyncio

from alembic import context
from app.models.base import Base
from app.models.user import *
from app.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import Connection, engine_from_config, pool



target_metadata = Base.metadata


def run_migrations(connection):
    context.configure(
        connection=connection,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


config = context.config

async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(str(settings.POSTGRES_URL), future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations)

    # configuration = config.get_section(config.config_ini_section)
    # assert configuration
    # configuration["sqlalchemy.url"] = settings.POSTGRES_URL.unicode_string()
    # connectable = AsyncEngine(
    #     engine_from_config(
    #         configuration=configuration,
    #         prefix="sqlalchemy.",
    #         poolclass=pool.NullPool,
    #         future=True,
    #     )
    # )
    # async with connectable.connect() as connection:
    #     await connection.run_sync(run_migrations)


asyncio.run(run_migrations_online())
