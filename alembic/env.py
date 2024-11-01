from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Añadir explícitamente el directorio `src` a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("sys.path:", sys.path)

from src.config import settings
from src.database import Base
from src.supplier.models import Supplier

# Configuración de Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ajustar la URL para que Alembic use una conexión síncrona
sync_database_url = settings.DATABASE_URL.replace("+asyncpg", "")
print("Original DATABASE_URL:", settings.DATABASE_URL)
print("Sync DATABASE_URL for Alembic:", sync_database_url)
config.set_main_option("sqlalchemy.url", sync_database_url)

target_metadata = Base.metadata
print("Target metadata:", target_metadata.tables.keys())

def run_migrations_offline() -> None:
    """Configura el contexto para migraciones sin conexión."""
    url = config.get_main_option("sqlalchemy.url")
    print("Running offline migrations with URL:", url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Configura el contexto para migraciones en línea."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    print("Running online migrations with connectable:", connectable)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
