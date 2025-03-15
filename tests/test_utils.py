import unittest
from datetime import datetime
from event_manager.event import Event
from event_manager.utils import get_event_weeks, get_events_in_range, count_weekly_events

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.events = [
            Event("Rent Payment", datetime(2024, 3, 1), recurrent_type="monthly", days=[1]),
            Event("Salary", datetime(2024, 3, 1), recurrent_type="monthly", days=[1, 15]),
            Event("Internet Bill", datetime(2024, 3, 15), recurrent_type="monthly", days=[15]),
            Event("Freelance Work", datetime(2026, 3, 3), recurrent_type="weekly", interval=2, days=[2]),
        ]

    def test_get_event_weeks(self):
        test_event = {
            "name": "Test Event",
            "start_date": datetime(2025, 3, 4),
            "end_date": datetime(2025, 6, 1),
            "recurrent_type": "weekly",
            "interval": 1,
            "days": [1, 16]
        }
        weeks = get_event_weeks(test_event)
        self.assertGreater(len(weeks), 0)

    def test_get_events_in_range(self):
        events = get_events_in_range(self.events, datetime(2024, 3, 1), datetime(2025, 3, 1))
        self.assertGreater(len(events), 0)

    def test_count_weekly_events(self):
        test_event = {
            "name": "Test Event",
            "start_date": datetime(2025, 3, 4),
            "end_date": datetime(2025, 6, 1),
            "recurrent_type": "weekly",
            "interval": 1,
            "days": [1, 16]
        }
        weekly_count = count_weekly_events(test_event, self.events)
        self.assertIsInstance(weekly_count, dict)

if __name__ == "__main__":
    unittest.main()