"""This module is used for configuring the Alembic environment prior to running
Alembic commands (such as; downgrade, upgrade .. etc)

"""
from logging.config import fileConfig
import pathlib
import sys
import time

from alembic import context
from chessdb_api import create_app
from chessdb_api.core.config_loader import DB_DSN
from chessdb_api.core.config_loader import DB_RETRY_INTERVAL
from chessdb_api.core.config_loader import DB_RETRY_LIMIT
from chessdb_api.core.db import DB
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Make migrations importable by adding the project root folder to the path.
# 'migrations/env.py == __file__
# 'migrations/' == parents[0] (the parent folder)
# '.' == parents[1] (the parents parent).
PROJECT_ROOT_DIR = str(pathlib.Path(__file__).parents[1])
sys.path.append(PROJECT_ROOT_DIR)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

app = create_app()
target_metadata = DB

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", str(DB_DSN))


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    retries = 0
    while True:
        try:
            retries += 1
            connection = connectable.connect()
        except Exception:
            if retries < DB_RETRY_LIMIT:
                time.sleep(DB_RETRY_INTERVAL)
            else:
                raise
        else:
            break

    with connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
