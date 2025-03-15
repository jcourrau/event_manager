from datetime import datetime, timedelta
from typing import List, Optional, Dict
import calendar
import logging

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

        if end_date and end_date < start_date:
            raise ValueError("End date must be before start date.")

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

            if not self._matches_monthly_interval(date):
                return False  # The month does not match the interval

            last_day = calendar.monthrange(date.year, date.month)[1]  # Get last valid day of the month

            # Adjust event days based on `use_last_day`
            valid_days = [
                day if day <= last_day else last_day  # Ensure days don't exceed the last day of the current month.
                for day in self.days  # Iterate through the specified days for this month.
            ] if self.use_last_day else self.days  # Use `last_day` adjustments only if `use_last_day` is enabled.

            return date.day in valid_days  # Check if the current day is within the valid days of the month.

        return False

    def _matches_weekly_interval(self, date: datetime) -> bool:
        """Checks if the date falls within the correct n-weekly interval."""
        logging.debug(f"=> Getting match for weekly interval on {date.strftime('%Y-%m-%d')} ({date.weekday()})")

        delta_days = (date - self.start_date).days
        weeks_since_start = delta_days // 7
        interval_mod = weeks_since_start % self.interval

        logging.debug(f"=> Delta days: {delta_days} | Weeks since start: {weeks_since_start} |Mod:  {interval_mod} {interval_mod == 0}")

        return interval_mod == 0

    def _matches_monthly_interval(self, date: datetime) -> bool:
        """Checks if the date falls within the correct monthly interval."""
        logging.debug(f"=> Getting match for monthly interval on {date.strftime('%Y-%m-%d')} ({date.weekday()})")

        months_since_start = (date.year - self.start_date.year) * 12 + (date.month - self.start_date.month)
        interval_mod = months_since_start % self.interval

        logging.debug(f"=> Weeks since start: {months_since_start} |Mod:  {interval_mod} {interval_mod == 0}")

        return interval_mod == 0

    def occurs_on_range(self, start_date: datetime, end_date: datetime) -> bool:
        """
        Check if the event could happen between the given dates. Meant for time ranges bigger than the interval.
        """

        return self.start_date <= end_date and (self.end_date is None or self.end_date >= start_date)

    def __str__(self):
        return (
            f"Event(name={self.name}, recurrent_type={self.recurrent_type}, "
            f"interval={self.interval}, start_date={self.start_date.strftime('%Y-%m-%d')}, "
            f"end_date={'None' if not self.end_date else self.end_date.strftime('%Y-%m-%d')}, "
            f"days={self.days})"
        )


'''----< Main Functions >----'''

