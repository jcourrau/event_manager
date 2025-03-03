from event_recurrance import *

existing_events = [
                      Event("Rent Payment", datetime(2024, 3, 1), recurrent_type="monthly", days_of_month=[1]),
                      Event("Gym Membership", datetime(2024, 3, 5), recurrent_type="monthly", days_of_month=[5]),
                      Event("Salary", datetime(2024, 3, 1), recurrent_type="monthly", days_of_month=[1, 15]),
                      Event("Electric Bill", datetime(2024, 3, 10), recurrent_type="monthly", days_of_month=[10]),
                      Event("Internet Bill", datetime(2024, 3, 15), recurrent_type="monthly", days_of_month=[15]),
                      Event("Netflix Subscription", datetime(2024, 3, 20), recurrent_type="monthly",
                            days_of_month=[20]),
                      Event("Coffee Subscription", datetime(2024, 3, 7), recurrent_type="monthly", days_of_month=[7]),
                      Event("Freelance Work", datetime(2024, 3, 3), recurrent_type="n-weekly", interval=2,
                            days_of_week=[2]),
                      Event("Spotify Subscription", datetime(2024, 3, 25), recurrent_type="monthly",
                            days_of_month=[25]),
                      Event("Groceries", datetime(2024, 3, 3), recurrent_type="n-weekly", interval=1,
                            days_of_week=[6]),
                      Event("Insurance Payment", datetime(2024, 3, 12), recurrent_type="monthly", days_of_month=[12]),
                      Event("Credit Card Payment", datetime(2024, 3, 22), recurrent_type="monthly",
                            days_of_month=[22]),
                      Event("Savings Deposit", datetime(2024, 3, 8), recurrent_type="n-weekly", interval=2,
                            days_of_week=[4]),
                      Event("Dining Out", datetime(2024, 3, 5), recurrent_type="n-weekly", interval=1,
                            days_of_week=[1, 5]),
                      Event("One-time Purchase", datetime(2024, 4, 12), datetime(2024, 4, 12)),
                  ] + [
                      Event(f"Expense {i}", datetime(2024, 3, i % 28 + 1), recurrent_type="n-weekly",
                            interval=i % 4 + 1, days_of_week=[i % 7])
                      for i in range(17, 50)
                  ]

if __name__ == "__main__":

    new_event_data = {
        "name": "Test Event",
        "start_date": datetime(2024, 3, 1),
        "recurrent_type": "n-weekly",
        "interval": 2,
        "days_of_week": [0, 4]  # Mondays and Thursdays
    }

    weekly_counts = count_weekly_events(new_event_data, existing_events)
    format_weekly_events(weekly_counts)
