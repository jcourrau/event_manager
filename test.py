import logging

from functions import *

# Configure logging
logging.basicConfig(
    level=logging.WARN,  # Set the logging level to DEBUG
    format="[%(levelname)s] | %(message)s"
)

# Reset existing_events by reassigning an empty list
existing_events = []

existing_events = [
                      Event("Rent Payment", datetime(2024, 3, 1), recurrent_type="monthly", days=[1]),
                      Event("Gym Membership", datetime(2025, 3, 5), recurrent_type="monthly", days=[5]),
                      Event("Salary", datetime(2024, 3, 1), recurrent_type="monthly", days=[1, 15]),
                      Event("Electric Bill", datetime(2024, 3, 10), recurrent_type="monthly", days=[10]),
                      Event("Internet Bill", datetime(2024, 3, 15), recurrent_type="monthly", days=[15]),
                      Event("Netflix Subscription", datetime(2024, 3, 20), recurrent_type="monthly",
                            days=[20]),
                      Event("Coffee Subscription", datetime(2024, 3, 7), recurrent_type="monthly", days=[7]),
                      Event("Freelance Work", datetime(2026, 3, 3), recurrent_type="n-weekly", interval=2,
                            days=[2]),
                      Event("Spotify Subscription", datetime(2024, 3, 25), recurrent_type="monthly",
                            days=[25]),
                      Event("Groceries", datetime(2024, 3, 3), recurrent_type="n-weekly", interval=1,
                            days=[6]),
                      Event("Insurance Payment", datetime(2024, 3, 12), recurrent_type="monthly", days=[12]),
                      Event("Credit Card Payment", datetime(2024, 3, 22), recurrent_type="monthly",
                            days=[22]),
                      Event("Savings Deposit", datetime(2025, 3, 8), recurrent_type="n-weekly", interval=2,
                            days=[4]),
                      Event("Dining Out", datetime(2025, 3, 5), recurrent_type="n-weekly", interval=1,
                            days=[1, 5]),
                      Event("One-time Purchase", datetime(2024, 4, 12), datetime(2024, 4, 12)),
                  ] + [
                      Event(f"Expense {i}", datetime(2024, 3, i % 28 + 1), recurrent_type="n-weekly",
                            interval=i % 4 + 1, days=[i % 7])
                      for i in range(17, 50)
                  ]

# TEST CASE
if __name__ == "__main__":


    test_case_1 = {
        "name": "Monday Sync",
        "start_date": datetime(2025, 3, 4),  # March 4, 2025 (Tuesday)
        "end_date": datetime(2025, 6, 1),
        "recurrent_type": "n-weekly",
        "interval": 1,
        "days": [1, 16]
    }

    # Relevant Weeks
    weeks = get_event_weeks(test_case_1)
    current_week = weeks[0]
    for i, week in enumerate(weeks):
        week_diff = week - current_week
        #print(f"{i+1:02d} | Week: {week.strftime('%Y-%m-%d')} | {week_diff.days} days")
        current_week = week

    # Relevant events
    '''You'd replace existing_events with existing_events = Event.objects.filter(end_date__isnull=True)'''
    test_end_date = test_case_1.get("end_date", None)
    events = get_events_in_range(event_list= existing_events, start_date= test_case_1["start_date"], end_date=test_end_date)
    for i, event in enumerate(events):
        end_date = event.end_date.strftime('%Y-%m-%d') if event.end_date else None
        #print(f"{i+1:02d} | {event.start_date.strftime('%Y-%m-%d')} - {end_date} | Event: {event.name}")

    #print(f"\nExcluded events:")
    excluded_events = [event for event in existing_events if event not in events]
    for i, event in enumerate(excluded_events):
        end_date = event.end_date.strftime('%Y-%m-%d') if event.end_date else None
        #print(f"{i+1:02d} | {event.start_date.strftime('%Y-%m-%d')} - {end_date} | Event: {event.name}")

    # Occurs on
    print(f"\n Occurs on {test_case_1["start_date"].strftime('%Y-%b-%a-%d')}")
    for event in existing_events:
        occurs = event.occurs_on(test_case_1["start_date"])
        if occurs:
         print(f"{occurs} | {event.name} | {event.recurrent_type} | {event.days}")

    # For each relevant week, calculate the relevant events (again) and count how many occur

    weekly_count = count_weekly_events(test_case_1, existing_events)
    print(weekly_count)


