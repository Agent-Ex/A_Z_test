"""Модуль для миграций Alembic."""

# STDLIB
from logging.config import fileConfig
import os

# THIRDPARTY
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# FIRSTPARTY
from app.database.db_prod_config import settings
from app.database.models import Base

# Константа для определения конфигурации алембика, по умолчанию под Docker.
IS_LOCAL = False  # Поменять на TRUE если миграции нужно сгенерировать локально

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if IS_LOCAL:
    # Конфигурация для генерации миграций локально.
    load_dotenv()
    external_port = os.environ.get('PROD_POSTGRES_DB_PORT')

    url = settings.get_db_url()
    local_alembic_url = url.set(host='localhost', port=external_port)

    config.set_main_option(
        'sqlalchemy.url',
        local_alembic_url.render_as_string(hide_password=False)
        + '?async_fallback=True',
    )
else:
    # Конфигурация под Docker Compose, когда миграции уже сгенерированы.
    config.set_main_option(
        'sqlalchemy.url',
        settings.get_db_url().render_as_string(hide_password=False)
        + '?async_fallback=True',
    )


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
