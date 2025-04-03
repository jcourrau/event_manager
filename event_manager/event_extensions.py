from sqlalchemy import Column, Float, Integer, String
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