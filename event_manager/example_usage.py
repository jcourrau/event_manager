from datetime import datetime
from uuid import uuid4
import event_manager as em
import pandas as pd


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.colheader_justify", "center")
pd.set_option("display.precision", 2)

# Simulated user_id (UUID style)
user_id = str(uuid4())

# Step 1: Create and store events
tx1 = em.Transaction(
    name="Gym Membership",
    start_date=datetime(2024, 3, 1),
    recurrent_type="monthly",
    interval=1,
    days=[1],
    amount=30.0,
    transaction_type="expense",
    user_id=user_id
)

tx2 = em.Transaction(
    name="Biweekly Salary",
    start_date=datetime(2024, 3, 1),
    recurrent_type="weekly",
    interval=2,
    days=[4],  # Friday
    amount=1000.0,
    transaction_type="income",
    user_id=user_id
)

tx3 = em.Transaction(
    name="Coffee Subscription",
    start_date=datetime(2024, 3, 3),
    recurrent_type="weekly",
    interval=1,
    days=[0],  # Monday
    amount=10.0,
    transaction_type="expense",
    user_id=user_id
)

# Save to DB
for tx in [tx1, tx2, tx3]:
    em.create_event(tx)

# Step 2: Query by user and date range
start = datetime(2024, 3, 1)
end = datetime(2024, 5, 1)
events = em.get_user_transactions(user_id, start, end)

# Step 3: Generate occurrence DataFrame
df = em.get_occurrence_df(events, start, end)
print("\nInitial Occurrences:\n", df)

# Step 4: Update events with amount > 20
for event in events:
    if hasattr(event, "amount") and event.amount > 20:
        em.update_event(event.id, {"amount": event.amount + 5})

# Step 5: Delete the coffee subscription
coffee_event = next((event for event in events if "Coffee" in event.name), None)
if coffee_event:
    em.delete_event(coffee_event.id)
    print(f"\nDeleted event: {coffee_event.name}")

# Step 6: Refresh and regenerate occurrences
updated_events = em.get_user_transactions(user_id, start, end)
updated_df = em.get_occurrence_df(updated_events, start, end)
print("\nUpdated Occurrences:\n", updated_df)
