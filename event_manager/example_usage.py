
from datetime import datetime
from event_manager.db_session import session_scope
from event_manager.event import Base
from event_manager.event_extensions import Transaction
from sqlalchemy import create_engine

engine = create_engine("sqlite:///events.db")
Base.metadata.create_all(engine)

# Run example inside context
with session_scope() as session:
    # Create transaction
    t = Transaction(
        name="Netflix",
        start_date=datetime(2024, 4, 1),
        recurrent_type="monthly",
        interval=1,
        days=[1],
        amount=12.99,
        transaction_type="expense",
        user_id="a1c43d23-9a1b-4a8c-bb62-5b14d989abcd"
    )
    session.add(t)

    # Modify
    t.amount = 14.99

    # Query
    txs = session.query(Transaction).filter_by(user_id=t.user_id).all()
    print("Transactions for user:", [str(tx) for tx in txs])

    # Delete
    session.delete(t)
