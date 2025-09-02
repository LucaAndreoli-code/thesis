import os
import string
import subprocess
import sys
from random import random

from sqlalchemy.orm import sessionmaker

from src.controller.v1.transaction import create_payment
from src.service.user import UserService

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text
from src.database.database import engine
from src.models import Base, Wallet, User, Transaction


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
        if not seed_initial_data():
            print("Attenzione: errore durante l'inserimento dei dati iniziali")
            return False
    else:
        print("Database has tables, checking migrations...")
        auto_migrate()

    print("Database ready!")
    return True

def seed_initial_data():
    print("Inserimento dati iniziali...")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        users_data = [
            {
                "username": "user1",
                "email": "user@example.com",
                "first_name": "User",
                "last_name": "One",
                "password": "password123"
            },
            {
                "username": "test",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "password123"
            },
            {
                "username": "mario",
                "email": "mario@example.com",
                "first_name": "Mario",
                "last_name": "Rossi",
                "password": "password123"
            }
        ]

        for user_data in users_data:
            UserService.create_user(session, user_data)

        wallets = session.query(Wallet).all()
        for wallet in wallets:
            wallet.balance = 100.00
            transactions = Transaction(
                from_wallet_id=None,
                to_wallet_id=wallet.id,
                amount=wallet.balance,
                description=f"First deposit to {wallet.wallet_number}",
                reference_code=f"TOP{os.urandom(4).hex().upper()}",
                status="completed",
                transaction_type="deposit"
            )
            session.add(transactions)

        session.commit()
        print(f"Creati {len(users_data)} utenti e i loro wallet con successo!")

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati iniziali: {e}")
        session.rollback()
        return False
    finally:
        session.close()

    return True
