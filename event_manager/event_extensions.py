from sqlalchemy import Column, Float, String
from datetime import datetime
from typing import List
from sqlalchemy import or_
from db_session import session_scope
from event import Event

# Example of extension
class Transaction(Event):
    """Extends Event to represent financial movements."""
    amount = Column(Float)
    transaction_type = Column(String(10))  # 'income', 'expense', 'savings'
    user_id = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "transaction"
    }

    def __init__(
            self, *,
            name: str,
            start_date,
            recurrent_type: str,
            interval: int,
            days,
            amount: float,
            transaction_type: str,
            user_id: str,
            end_date=None,
            use_last_day=False
    ):

        super().__init__(
            name=name,
            start_date=start_date,
            end_date=end_date,
            recurrent_type=recurrent_type,
            interval=interval,
            days=days,
            use_last_day=use_last_day,
            subclass="transaction"
        )

        # Initial Exceptions.
        transaction_type = transaction_type.lower()
        if transaction_type not in ["income", "expense", "savings"]:
            raise ValueError("Transaction type must be 'income', 'expense' or 'savings'")

        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be of type 'int' or 'float'")



        self.amount = abs(amount)
        self.transaction_type = transaction_type  # Income, Expense...
        self.user_id = str(user_id)

    def __repr__(self):
        return (f"<Transaction(name='{self.name}', type='{self.transaction_type}', "
                f"amount={self.amount}, user_id={self.user_id}, start={self.start_date}, "
                f"recurrence='{self.recurrent_type}')>")

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.name}: ${self.amount}"



def get_user_transactions(user_id: str, start: datetime, end: datetime) -> List[Transaction]:
    """
    Returns user transactions whose active date ranges overlap with the provided period.
    """
    with session_scope() as session:
        txs = session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.start_date <= end,
            or_(
                Transaction.end_date == None,
                Transaction.end_date >= start
            )
        ).all()

        # Create independent copies of transactions with the original ID
        detached = []
        for tx in txs:
            new_tx = Transaction(
                name=tx.name,
                start_date=tx.start_date,
                end_date=tx.end_date,
                recurrent_type=tx.recurrent_type,
                interval=tx.interval,
                days=tx.days,
                use_last_day=tx.use_last_day,
                transaction_type=tx.transaction_type,
                amount=tx.amount,
                user_id=tx.user_id
            )
            new_tx.id = tx.id  # Preserve original database ID
            detached.append(new_tx)

        print("Preloaded: ", [(tx.name, tx.start_date) for tx in txs])

        return detached

