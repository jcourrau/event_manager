from datetime import datetime, timedelta
from typing import List, Optional, Dict

class Event:
    def __init__(
        self, name: str, start_date: datetime, end_date: Optional[datetime] = None,
        recurrent_type: str = "n-weekly", interval: int = 1,
        days_of_week: Optional[List[int]] = None, days_of_month: Optional[List[int]] = None
    ):
        """
        Base Event class for handling recurring events.
        :param name: Event name
        :param start_date: The first occurrence of the event
        :param end_date: The last occurrence of the event (optional, defaults to no end)
        :param recurrent_type: "n-weekly" or "monthly"
        :param interval: Recurrence interval (1-12 weeks max for weekly events)
        :param days_of_week: List of weekdays the event occurs (0=Monday, 6=Sunday)
        :param days_of_month: List of month days the event occurs (1-31)
        """
        if recurrent_type == "n-weekly" and (interval < 1 or interval > 12):
            raise ValueError("Interval must be between 1 and 12 weeks.")

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.recurrent_type = recurrent_type
        self.interval = interval
        self.days_of_week = days_of_week or []
        self.days_of_month = days_of_month or []

    def occurs_on(self, date: datetime) -> bool:
        """Checks if the event occurs on the given date."""
        if self.start_date > date or (self.end_date and self.end_date < date):
            return False  # Outside valid date range

        if self.recurrent_type == "n-weekly":
            return date.weekday() in self.days_of_week and self._matches_weekly_interval(date)

        if self.recurrent_type == "monthly":
            return date.day in self.days_of_month

        return False

    def _matches_weekly_interval(self, date: datetime) -> bool:
        """Checks if the date falls within the correct n-weekly interval."""
        delta_days = (date - self.start_date).days
        weeks_since_start = delta_days // 7
        return weeks_since_start % self.interval == 0

    def __str__(self):
        return (
            f"Event(name={self.name}, recurrent_type={self.recurrent_type}, "
            f"interval={self.interval}, start_date={self.start_date.strftime('%Y-%m-%d')}, "
            f"end_date={'None' if not self.end_date else self.end_date.strftime('%Y-%m-%d')}, "
            f"days_of_week={self.days_of_week}, days_of_month={self.days_of_month})"
        )


def get_events_in_range(start_date: datetime, end_date: datetime, event_queryset: List[Event]) -> List[Event]:
    """Returns all events that may occur within the given date range."""
    if not end_date:
        end_date = start_date + timedelta(weeks=52)  # Default max 1-year range if no end date

    return [
        event for event in event_queryset
        if event.start_date <= end_date and (event.end_date is None or event.end_date >= start_date)
    ]

def count_events(start_date: datetime, end_date: datetime, event_queryset: List[Event]) -> int:
    """Counts the total number of events occurring within the given date range."""
    relevant_events = get_events_in_range(start_date, end_date, event_queryset)
    return sum(1 for event in relevant_events for day in range((end_date - start_date).days + 1)
               if event.occurs_on(start_date + timedelta(days=day)))


def week_range(target_date: datetime) -> (datetime, datetime):
    """Returns the Monday (start) and Sunday (end) of the given week."""
    start_of_week = target_date - timedelta(days=target_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week


def get_event_weeks(event_data: Dict, week_limit: int = 42) -> List[datetime]:
    """Returns the Mondays of the weeks in which the event would occur, limited by week_limit."""
    start_date = event_data["start_date"]
    end_date = event_data.get("end_date")
    interval = event_data.get("interval", 1)

    week_batch = week_limit // 3
    weeks = []

    if end_date:
        total_weeks = (end_date - start_date).days // 7
        if total_weeks > week_limit:
            first_middle_week = int((total_weeks / 2) - (week_batch / 2) + 1)
            last_middle_week = int((total_weeks / 2) + (week_batch / 2) - 1)
            weeks += [start_date + timedelta(weeks=w) for w in range(0, week_batch)]  # First batch
            weeks += [start_date + timedelta(weeks=w) for w in range(first_middle_week, last_middle_week, week_batch // 3)]  # Middle batch
            weeks += [end_date - timedelta(weeks=w) for w in range(week_batch)]  # Last batch
        else:
            weeks += [start_date + timedelta(weeks=w) for w in range(0, total_weeks + 1)]
    else:
        weeks += [start_date + timedelta(weeks=w) for w in range(0, week_limit)]

    return [week_range(week)[0] for week in weeks]  # Get only Mondays


def count_weekly_events(new_event_data: Dict, event_queryset: List[Event]) -> Dict[datetime, int]:
    """Counts the number of events per week that would occur if a new event is added."""
    event_weeks = get_event_weeks(new_event_data)
    weekly_event_counts = {}

    for monday_date in event_weeks:
        start_of_week, end_of_week = week_range(monday_date)
        weekly_event_counts[start_of_week] = count_events(start_of_week, end_of_week, event_queryset)

    return weekly_event_counts

def format_weekly_events(weekly_event_counts: Dict[datetime, int]) -> None:
    """Formats and prints weekly event counts in a readable way with date format m/d/yyyy."""
    print("Weekly Events:")
    total = 0
    counter = 0
    for week_start, count in sorted(weekly_event_counts.items()):
        formatted_date = week_start.strftime("%m/%d/%Y")
        print(f"Week {formatted_date}: {count} events")
        total += count
        counter += 1

def summary_weekly_events(weekly_event_counts: Dict[datetime, int]) -> str:
    """Formats and prints weekly event counts in a readable way with date format m/d/yyyy."""
    total = 0
    counter = 0
    for week_start, count in sorted(weekly_event_counts.items()):
        formatted_date = week_start.strftime("%m/%d/%Y")
        # print(f"Week {formatted_date}: {count} events")
        total += count
        counter += 1
    return f"Total events: {total} | Total weeks: {counter} | Average events per week: {total/counter: .0f}"