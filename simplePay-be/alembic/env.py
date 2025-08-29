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

# Metodo più robusto per trovare la root del progetto
current_dir = Path(__file__).parent  # cartella alembic/
root_dir = current_dir.parent        # cartella simplePay-be/

# Aggiungi al Python path
sys.path.insert(0, str(root_dir))

# Debug del path
print(f"Current dir: {current_dir}")
print(f"Root dir: {root_dir}")
print(f"Python path: {sys.path[0]}")

# Ora prova gli import
try:
    from src.models.user import User
    print("✅ User imported successfully")
except ImportError as e:
    print(f"❌ Failed to import User: {e}")

try:
    from src.models.wallet import Wallet
    print("✅ Wallet imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Wallet: {e}")

try:
    from src.models.transaction import Transaction
    print("✅ Transaction imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Transaction: {e}")

try:
    from src.models import Base
    print("✅ Base imported successfully")
    print(f"Tables in Base: {list(Base.metadata.tables.keys())}")
except ImportError as e:
    print(f"❌ Failed to import Base: {e}")

target_metadata = Base.metadata if 'Base' in locals() else None

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()