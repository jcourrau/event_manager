import unittest
from datetime import datetime
from event_manager.event import Event

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event = Event("Test Event", datetime(2024, 3, 1), recurrent_type="monthly", days=[1])

    def test_occurs_on(self):
        self.assertTrue(self.event.occurs_on(datetime(2024, 4, 1)))
        self.assertFalse(self.event.occurs_on(datetime(2024, 4, 2)))

    def test_occurrences_in_range(self):
        occurrences = self.event.get_occurrences(datetime(2024, 3, 1), datetime(2025, 3, 1))
        self.assertGreater(len(occurrences), 0)

if __name__ == "__main__":
    unittest.main()