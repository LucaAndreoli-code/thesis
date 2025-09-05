from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.models import Base
from src.models.user import User
from src.models.wallet import Wallet
from src.models.transaction import Transaction
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

if 'pytest' in sys.modules or 'pytest' in ' '.join(sys.argv):
    load_dotenv('.env.test', override=True)
else:
    load_dotenv('.env')

target_metadata = Base.metadata if 'Base' in locals() else None
config = context.config

# override config with env variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
if DATABASE_URL:
    config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()