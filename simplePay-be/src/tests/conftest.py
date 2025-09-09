import pytest
import os
import sys
from sqlalchemy import text

from migration_manager import setup_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.database import engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    print("\nReset database for tests...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()
        setup_database()

    yield