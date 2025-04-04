import calendar
import logging
from datetime import datetime
from typing import List, Optional, TypedDict
import pandas as pd
from sqlalchemy import  Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EventDict(TypedDict):
    name: str
    start_date: datetime
    end_date: Optional[datetime]
    recurrent_type: str
    interval: int
    days: List[int]

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    recurrent_type = Column(String(20))  # 'weekly' or 'monthly'
    interval = Column(Integer, default=1)
    days = Column(JSON, default=list)
    event_type = Column(String(50))  # Defines whether it's an 'event' or 'transaction'
    use_last_day = Column(Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "event",
        "polymorphic_on": event_type
    }

    def __init__(
        self, *,
        name: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        recurrent_type: str = "weekly",
        interval: int = 1,
        days: Optional[List[int]] = None,
        use_last_day: Optional[bool] = False,
        subclass: str = "event"
    ):
        """
        Initializes an Event instance or one of its subclasses.

        :param name: Name of the event.
        :param start_date: The first date the event occurs.
        :param end_date: Optional end date. If not provided, the event continues indefinitely.
        :param recurrent_type: Either "weekly" or "monthly". Determines how recurrence is calculated.
        :param interval: Interval of recurrence. For example, every 2 weeks or every 3 months.
        :param days: A list of days the event occurs.
                      - For weekly events: integers 0–6 (0 = Monday, 6 = Sunday).
                      - For monthly events: integers 1–31 representing days of the month.
        :param use_last_day: If True, the event will also occur on the last day of the month (when applicable).
        :param subclass: Internal use for subclass identity in polymorphic inheritance (e.g., "transaction").
        """

        # Initial Exceptions.
        if recurrent_type not in ["weekly", "monthly"]:
            raise ValueError("Recurrent type must be 'weekly' or 'monthly'")

        if recurrent_type == "weekly":
            if not 1 <= interval <= 12:
                raise ValueError("Interval must be between 1 and 12 weeks.")
            if days and not all(0 <= day <= 6 for day in days):
                raise ValueError("Days for weekly events must be between 0 (Mon) and 6 (Sun).")

        elif recurrent_type == "monthly":
            if interval != 1:
                raise ValueError("Monthly events can only recur every 1 month.")
            if days and not all(1 <= day <= 31 for day in days):
                raise ValueError("Days for monthly events must be between 1 and 31.")

        if end_date and end_date < start_date:
            raise ValueError("End date must be after start date.")

        # Initial Values
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.recurrent_type = recurrent_type
        self.interval = interval
        self.days = days if days is not None else [start_date.weekday()]
        self.use_last_day = use_last_day
        self.event_type = subclass


    def get_occurrences(self, start_date: datetime, end_date: datetime):
        if not self.occurs_on_range(start_date, end_date):
            logging.debug(f"Event {self.name} does not occur on the given date range")
            return []  # Returning an empty list is more predictable than None

        return [date for date in pd.date_range(start=start_date, end=end_date) if self.occurs_on(date)]

    def occurs_on(self, date: datetime) -> bool:
        """Checks if the event occurs on the given date."""

        if self.start_date > date or (self.end_date and self.end_date < date):
            return False  # Outside valid date range

        if self.recurrent_type == "weekly":
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
        """Checks if the date falls within the correct weekly
        interval."""
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
