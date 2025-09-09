import os
import subprocess
import sys
from decimal import Decimal
from sqlalchemy.orm import sessionmaker
from src.service.transaction import TransactionService
from src.service.user import UserService

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text
from src.database.database import engine
from src.models import Base, Wallet, Transaction


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
    print("Initializing data...")

    Session = sessionmaker(bind=engine)
    db = Session()

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
            UserService(db).create_user(user_data)

        wallets = db.query(Wallet).all()
        wallet_balances = {wallet.id: 0.0 for wallet in wallets}

        all_transactions = []

        for wallet in wallets:
            initial_deposit = 1000.00
            deposit_transaction = TransactionService(db).create_transaction(
                from_wallet_id=None,
                to_wallet_id=wallet.id,
                amount=initial_deposit,
                description=f"First deposit to {wallet.wallet_number}",
                transaction_type="deposit",

            )
            all_transactions.append(deposit_transaction)
            wallet_balances[wallet.id] += initial_deposit

        # Transazione 1: Wallet 1 -> Wallet 2
        transaction_user_from_1 = TransactionService(db).create_transaction(
            from_wallet_id=1,
            to_wallet_id=2,
            amount=12.34,
            description=f"Payment to {users_data[1]['email']}",
            transaction_type="send",

        )
        all_transactions.append(transaction_user_from_1)
        wallet_balances[1] -= 12.34
        wallet_balances[2] += 12.34

        transaction_user_to_1 = TransactionService(db).create_transaction(
            from_wallet_id=2,
            to_wallet_id=1,
            amount=12.34,
            description=f"Receiving from {users_data[0]['email']}",
            transaction_type="receive",
        )
        all_transactions.append(transaction_user_to_1)

        # Transazione 2: Wallet 1 -> Wallet 3
        transaction_user_from_2 = TransactionService(db).create_transaction(
            from_wallet_id=1,
            to_wallet_id=3,
            amount=25.50,
            description=f"Payment to {users_data[2]['email']}",
            transaction_type="send",
        )
        all_transactions.append(transaction_user_from_2)
        wallet_balances[1] -= 25.50
        wallet_balances[3] += 25.50

        transaction_user_to_2 = TransactionService(db).create_transaction(
            from_wallet_id=3,
            to_wallet_id=1,
            amount=25.50,
            description=f"Receiving from {users_data[0]['email']}",
            transaction_type="receive",

        )
        all_transactions.append(transaction_user_to_2)

        # Transazione 3: Wallet 2 -> Wallet 3
        transaction_user_from_3 = TransactionService(db).create_transaction(
            from_wallet_id=2,
            to_wallet_id=3,
            amount=33.75,
            description=f"Payment to {users_data[2]['email']}",
            transaction_type="send",

        )
        all_transactions.append(transaction_user_from_3)
        wallet_balances[2] -= 33.75
        wallet_balances[3] += 33.75

        transaction_user_to_3 = TransactionService(db).create_transaction(
            from_wallet_id=3,
            to_wallet_id=2,
            amount=33.75,
            description=f"Receiving from {users_data[1]['email']}",
            transaction_type="receive",

        )
        all_transactions.append(transaction_user_to_3)

        # Transazione 4: Wallet 3 -> Wallet 1
        transaction_user_from_4 = TransactionService(db).create_transaction(
            from_wallet_id=3,
            to_wallet_id=1,
            amount=45.20,
            description=f"Payment to {users_data[0]['email']}",
            transaction_type="send",

        )
        all_transactions.append(transaction_user_from_4)
        wallet_balances[3] -= 45.20
        wallet_balances[1] += 45.20

        transaction_user_to_4 = TransactionService(db).create_transaction(
            from_wallet_id=1,
            to_wallet_id=3,
            amount=45.20,
            description=f"Receiving from {users_data[2]['email']}",
            transaction_type="receive",

        )
        all_transactions.append(transaction_user_to_4)

        # Transazione 5: Wallet 2 -> Wallet 1
        transaction_user_from_5 = TransactionService(db).create_transaction(
            from_wallet_id=2,
            to_wallet_id=1,
            amount=64.30,
            description=f"Payment to {users_data[0]['email']}",
            transaction_type="send",

        )
        all_transactions.append(transaction_user_from_5)
        wallet_balances[2] -= 64.30
        wallet_balances[1] += 64.30

        transaction_user_to_5 = TransactionService(db).create_transaction(
            from_wallet_id=1,
            to_wallet_id=2,
            amount=64.30,
            description=f"Receiving from {users_data[1]['email']}",
            transaction_type="receive",

        )
        all_transactions.append(transaction_user_to_5)

        # Transazione di prelievo
        withdraw_amount = 64.30
        withdraw_transaction = TransactionService(db).create_transaction(
            from_wallet_id=1,
            to_wallet_id=None,
            amount=withdraw_amount,
            description="Bank withdrawal - Utente Prova",
            transaction_type="withdraw",

        )
        all_transactions.append(withdraw_transaction)
        wallet_balances[1] -= withdraw_amount

        # Aggiorna i saldi dei wallet
        for wallet in wallets:
            wallet.balance = wallet_balances[wallet.id]

        # Salva tutte le transazioni
        for transaction in all_transactions:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)

        # Commit finale
        db.commit()
        print(
            f"Users created: {len(users_data)}, {len(wallets)} wallet and {len(all_transactions)} transactions!")

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati iniziali: {e}")
        db.rollback()
        return False
    finally:
        db.close()

    return True