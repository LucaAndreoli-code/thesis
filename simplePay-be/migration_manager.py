import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text
from src.database.database import engine
from src.models import Base


def run_command(cmd):
    cwd = os.path.dirname(os.path.abspath(__file__))

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    output = result.stdout + result.stderr
    return result.returncode == 0, output

def auto_migrate():
    print("Check migrations...")

    success, output = run_command("alembic check")
    if success:
        print("Database up-to-date, no migrations needed.")
        return True

    print("Found differences, creating migration...")
    success, output = run_command("alembic revision --autogenerate -m 'Auto update'")

    if "No changes in schema detected" in output:
        print("Database up-to-date, no migrations needed.")
        return True

    if success:
        print("Migration file created.")
        success, output = run_command("alembic upgrade head")
        if success:
            print("Migration applied successfully.")
            return True
        else:
            print(f"Migration Error: {output}")
    else:
        print(f"Creating migration error: {output}")

    return False


def setup_database():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
    except Exception as e:
        print(f"Connection error: {e}")
        quit()

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if len(tables) == 0:
        print("Database is empty, creating tables...")
        Base.metadata.create_all(bind=engine)
        run_command("alembic stamp head")
        print("Database initialized with tables.")
    else:
        print("Database has tables, checking migrations...")
        auto_migrate()

    print("Database ready!")
    return True