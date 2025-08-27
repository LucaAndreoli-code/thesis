from sqlalchemy.orm import Session
from typing import Optional, List
from decimal import Decimal
from . import User, Wallet, Transaction, WalletType, TransactionType, Notification


class ModelUtils:
    """Utility class for common model operations"""

    @staticmethod
    def create_user_with_wallet(
            db: Session,
            username: str,
            email: str,
            password_hash: str,
            first_name: str,
            last_name: str,
            wallet_type_code: str = "BASIC"
    ) -> User:
        """Create a new user with a default wallet"""

        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.flush()  # Get user ID

        # Get wallet type
        wallet_type = db.query(WalletType).filter(
            WalletType.type_code == wallet_type_code
        ).first()

        if not wallet_type:
            raise ValueError(f"Wallet type {wallet_type_code} not found")

        # Create wallet
        wallet = Wallet(
            user_id=user.id,
            wallet_type_id=wallet_type.id,
            wallet_number=Wallet.generate_wallet_number()
        )
        db.add(wallet)

        # Create welcome notification
        notification = Notification.create_system_notification(
            user_id=user.id,
            title="Benvenuto in Simple Pay!",
            message=f"Il tuo conto {wallet.wallet_number} è stato creato con successo.",
            notification_type="account_created"
        )
        db.add(notification)

        db.commit()
        return user

    @staticmethod
    def transfer_money(
            db: Session,
            from_wallet_id: int,
            to_wallet_id: int,
            amount: Decimal,
            description: str = None,
            transaction_type_code: str = "TRANSFER"
    ) -> Transaction:
        """Transfer money between wallets"""

        # Get wallets
        from_wallet = db.query(Wallet).filter(Wallet.id == from_wallet_id).first()
        to_wallet = db.query(Wallet).filter(Wallet.id == to_wallet_id).first()

        if not from_wallet or not to_wallet:
            raise ValueError("One or both wallets not found")

        if not from_wallet.can_withdraw(amount):
            raise ValueError("Insufficient funds")

        # Get transaction type
        transaction_type = db.query(TransactionType).filter(
            TransactionType.type_code == transaction_type_code
        ).first()

        if not transaction_type:
            raise ValueError(f"Transaction type {transaction_type_code} not found")

        # Calculate fee
        fee_amount = transaction_type.calculate_fee(amount)

        # Create transaction
        transaction = Transaction(
            from_wallet_id=from_wallet_id,
            to_wallet_id=to_wallet_id,
            transaction_type_id=transaction_type.id,
            amount=amount,
            description=description,
            reference_code=Transaction.generate_reference_code(),
            fee_amount=fee_amount
        )
        db.add(transaction)
        db.flush()  # Get transaction ID

        # Update balances
        total_amount = amount + fee_amount
        from_wallet.balance -= total_amount
        from_wallet.available_balance -= total_amount
        to_wallet.balance += amount
        to_wallet.available_balance += amount

        # Complete transaction
        transaction.complete_transaction()

        # Create notifications
        sender_notification = Notification.create_transaction_notification(
            user_id=from_wallet.user_id,
            transaction_id=transaction.id,
            notification_type="transaction_completed",
            title="Bonifico inviato",
            message=f"Hai inviato €{amount} a {to_wallet.wallet_number}"
        )

        recipient_notification = Notification.create_transaction_notification(
            user_id=to_wallet.user_id,
            transaction_id=transaction.id,
            notification_type="transaction_completed",
            title="Bonifico ricevuto",
            message=f"Hai ricevuto €{amount} da {from_wallet.wallet_number}"
        )

        db.add(sender_notification)
        db.add(recipient_notification)
        db.commit()

        return transaction

    @staticmethod
    def get_user_transaction_history(
            db: Session,
            user_id: int,
            limit: int = 50,
            offset: int = 0
    ) -> List[Transaction]:
        """Get transaction history for a user"""

        user_wallets = db.query(Wallet.id).filter(Wallet.user_id == user_id).subquery()

        transactions = db.query(Transaction).filter(
            (Transaction.from_wallet_id.in_(user_wallets)) |
            (Transaction.to_wallet_id.in_(user_wallets))
        ).order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()

        return transactions

    @staticmethod
    def get_user_balance_summary(db: Session, user_id: int) -> dict:
        """Get balance summary for all user wallets"""

        wallets = db.query(Wallet).filter(
            Wallet.user_id == user_id,
            Wallet.status == "active"
        ).all()

        total_balance = sum(wallet.balance for wallet in wallets)
        total_available = sum(wallet.available_balance for wallet in wallets)

        return {
            "total_balance": total_balance,
            "total_available_balance": total_available,
            "wallet_count": len(wallets),
            "wallets": [
                {
                    "id": wallet.id,
                    "wallet_number": wallet.wallet_number,
                    "balance": wallet.balance,
                    "available_balance": wallet.available_balance,
                    "wallet_type": wallet.wallet_type.type_name
                }
                for wallet in wallets
            ]
        }

    @staticmethod
    def mark_all_notifications_as_read(db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user"""

        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})

        db.commit()
        return count