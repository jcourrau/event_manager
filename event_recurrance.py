from datetime import datetime, timedelta
from doctest import debug
from typing import List, Optional, Dict
import calendar

class Event:
    def __init__(
        self, name: str, start_date: datetime, end_date: Optional[datetime] = None,
        recurrent_type: str = "n-weekly", interval: int = 1,
        days: Optional[List[int]] = None, use_last_day: Optional[bool] = False
    ):
        """
        Base Event class for handling recurring events.
        :type days: object
        :param name: Event name
        :param start_date: The first occurrence of the event
        :param end_date: The last occurrence of the event (optional, defaults to no end)
        :param recurrent_type: "n-weekly" or "monthly" defines if days are calculated for week or month
        :param interval: Recurrence interval (1-12 weeks max for weekly events)
        :param days: List of weekdays or month days the event occurs (0=Monday, 6=Sunday or 1st and 15th)
        :param use_last_day: Whether to use last day of the month. (optional, defaults to False)
        """
        if recurrent_type not in ["n-weekly", "monthly"]:
            raise ValueError("Recurrent type must be 'n-weekly' or 'monthly'")

        if recurrent_type == "n-weekly":
            if interval < 1 or interval > 12:
                raise ValueError("Interval must be between 1 and 12 weeks.")
        elif interval != 1:
            raise ValueError(f"Interval can't be greater than 1 month.")

        if recurrent_type == "n-weekly" and days and max(days) > 7:
            raise ValueError("The maximum days of the week must be 7.")

        if recurrent_type == "monthly" and days and max(days) > 31:
            raise ValueError("The maximum days of the month must be 31.")

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.recurrent_type = recurrent_type
        self.interval = interval
        self.days = days or []
        self.use_last_day = use_last_day

    def occurs_on(self, date: datetime) -> bool:
        """Checks if the event occurs on the given date."""

        if self.start_date > date or (self.end_date and self.end_date < date):
            return False  # Outside valid date range

        if self.recurrent_type == "n-weekly":
            return date.weekday() in self.days and self._matches_weekly_interval(date)

        if self.recurrent_type == "monthly":
            last_day = calendar.monthrange(date.year, date.month)[1]  # Get last valid day of the month

            # Adjust event days based on `use_last_day`
            valid_days = [
                day if day <= last_day else last_day
                for day in self.days
            ] if self.use_last_day else self.days

            return date.day in valid_days

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
            f"days={self.days})"
        )


'''----< Main Functions >----'''


def get_events_in_range(start_date: datetime, end_date: datetime, event_list: List[Event]) -> List[Event]:
    """Returns all events that may occur within the given date range."""
    if not end_date:
        end_date = start_date + timedelta(weeks=52)  # Default max 1-year range if no end date

    return [
        event for event in event_list
        if event.start_date <= end_date and (event.end_date is None or event.end_date >= start_date)
    ]

# start | date,  end | date => count | int
def count_events(start_date: datetime, end_date: datetime, event_list: List[Event]) -> int:
    """Counts the total number of events occurring within the given date range efficiently,
    only checking dates when events actually occur.
    """
    relevant_events = get_events_in_range(start_date, end_date, event_list)
    event_count = 0

    for event in relevant_events:
        # Generate a list of dates where the event actually occurs
        current_date = event.start_date

        while current_date <= end_date:
            if event.occurs_on(current_date):  # Check only actual event dates
                event_count += 1

            # Move to the next possible event occurrence
            if event.recurrent_type == "n-weekly":
                current_date += timedelta(weeks=event.interval)  # Skip directly to the next expected week

            elif event.recurrent_type == "monthly":
                # Handle monthly recurrences safely
                next_month = current_date.month + event.interval
                next_year = current_date.year + (next_month - 1) // 12
                next_month = (next_month - 1) % 12 + 1
                day = min(current_date.day, calendar.monthrange(next_year, next_month)[1])  # Avoid overflow
                current_date = datetime(next_year, next_month, day)

            else:
                current_date += timedelta(days=1)  # Default fallback (shouldn't happen)

    return event_count

# date => mon - sun | dates
def week_range(target_date: datetime) -> (datetime, datetime):
    """Returns the Monday (start) and Sunday (end) of the given week."""
    start_of_week = target_date - timedelta(days=target_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

# event | dic => week: count | dict
def get_event_weeks(event_data: Dict, week_limit: int = 42) -> List[datetime]:
    """Returns a list of Mondays representing the weeks in which the event occurs,
    with a limit of `week_limit` weeks. If the event duration exceeds this limit,
    the function selects representative weeks from three key periods (start, middle, end)."""

    start_date = event_data["start_date"]
    end_date = event_data.get("end_date")
    # Interval for weekly recurrence
    interval = event_data.get("interval", 1) if event_data.get("recurrent_type") == "n-weekly" else 30

    if end_date: # If the event has a defined end date
        total_weeks = (end_date - start_date).days // interval # Calculate the total duration in weeks

        if total_weeks > week_limit: # If the total duration exceeds the limit, use batches.
            batch_size = week_limit // 3  # Divide the week limit into three batches
            remaining_weeks = week_limit - (2 * batch_size)  # Weeks to distribute evenly

            first_batch = [start_date + timedelta(weeks=w) for w in range(batch_size)]
            last_batch = [end_date - timedelta(weeks=w) for w in range(batch_size)]

            # Evenly distribute remaining weeks
            step = (total_weeks - 2 * batch_size) / (remaining_weeks + 1)  # Compute step size
            distributed_weeks = [
                start_date + timedelta(weeks=int(batch_size + step * i))  # Evenly spaced weeks
                for i in range(remaining_weeks)
            ]

            selected_weeks = first_batch + distributed_weeks + last_batch  # Combine all weeks


        else:
            # If within limit, include all weeks from start to end
            selected_weeks = [start_date + timedelta(weeks=w) for w in range(total_weeks + 1)]
    else:
        # If no end date, generate weeks up to the predefined limit
        selected_weeks = [start_date + timedelta(weeks=w * interval) for w in range(week_limit)]

    return [week_range(week)[0] for week in selected_weeks]  # Return only Mondays

# event | dic, event | obj_list => week:count dic
def count_weekly_events(new_event_data: Dict, event_list: List[Event]) -> Dict[datetime, int]:
    """Counts the number of events per week that would occur if a new event is added."""
    event_weeks = get_event_weeks(new_event_data)
    weekly_event_counts = {}

    for this_week in event_weeks:
        start_of_week, end_of_week = week_range(this_week)
        weekly_event_counts[start_of_week] = count_events(start_of_week, end_of_week, event_list)

    return weekly_event_counts

'''----< Other Functions >----'''

def format_weekly_events(weekly_event_counts: Dict[datetime, int]) -> None:
    """Formats and prints weekly event counts in a readable way with date format m/d/yyyy."""
    # print("Weekly Events:")
    total = 0
    counter = 0
    for week_start, count in sorted(weekly_event_counts.items()):
        formatted_date = week_start.strftime("%m/%d/%Y")
        # print(f"Week {formatted_date}: {count} events")
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