from datetime import datetime, timedelta
import pandas as pd
from .event import Event, EventDict
from typing import List, Union
import logging

# event parameters | dic , week_limit | 48 int =>  week_start_date(week_limit) | list
def get_event_weeks(event: Union[Event, EventDict], week_limit=48):
    """
    Determines event recurrence and returns a list of weeks (Mondays) when the event occurs.
    Supports both Event objects and dictionary-based event representations.

    :param event: An Event instance or a dictionary containing event data.
    :param week_limit: Number of weeks to retrieve.
    :return: List of week start dates.
    """
    if isinstance(event, dict):
        event = Event(
            name=event["name"],
            start_date=event["start_date"],
            end_date=event.get("end_date"),
            recurrent_type=event["recurrent_type"],
            interval=event["interval"],
            days=event["days"]
        )

    start_date = event.start_date
    end_date = event.end_date or (start_date + timedelta(weeks=week_limit * event.interval))
    interval = event.interval
    recurrent_type = event.recurrent_type

    if (end_date - start_date).days > 1825:
        raise ValueError("Can't get weeks for more than 5 years")

    if recurrent_type == "weekly":
        if interval < 1 or interval > 12:
            raise ValueError("Interval must be between 1 and 12 weeks.")
    elif interval != 1:
        raise ValueError(f"Interval can't be greater than 1 month.")


    if recurrent_type == "weekly":
        start_date = start_date - timedelta(days=start_date.weekday())  # Ensure start_date aligns to Monday
        date_range = pd.date_range(start=start_date, end=end_date, freq=f'{interval * 7}D')
        relevant_weeks_df = pd.DataFrame(date_range, columns=['week_start_date'])


    elif recurrent_type == "monthly":
        days = event.days
        date_range = pd.date_range(start=start_date, end=end_date)
        relevant_dates = {date for date in date_range if date.day in days}

        # Apply interval filtering
        relevant_months = []
        last_added_month = None
        for date in sorted(relevant_dates):
            if last_added_month is None or (date.year * 12 + date.month) >= last_added_month + interval:
                relevant_months.append(date)
                last_added_month = date.year * 12 + date.month

        relevant_weeks = [date - timedelta(days=date.weekday()) for date in relevant_months]


        relevant_weeks_df = pd.DataFrame(relevant_weeks, columns=["week_start_date"])

    else:
        raise ValueError("Unknown recurrent type")

    return _get_batched_weeks(relevant_weeks_df, week_limit)['week_start_date'].tolist()

# week_start_date | DateFrame =>  batch_records(sample_size) | DataFrame
def _get_batched_weeks(df, sample_size):
    """
    Returns the first and last batch_size rows, and the evenly
    distribute batch_size rows in the middle of the DataFrame.

    :param df: DataFrame with dates.
    :param sample_size: total number of rows to sample.
    :return: DataFrame with selected rows.
    """

    batch_size = sample_size // 3


    if len(df) <= sample_size:
        logging.debug(f"\n=> Week count ({len(df)}) is less than or equal to sample size ({sample_size})")
        logging.debug("<= Returning all weeks.")
        return df  # If there are not enough rows.

    logging.debug(f"\nBatching {len(df)} weeks | In 3 batches of {batch_size} weeks | Sample size: {sample_size}")
    first_n = df.head(batch_size)
    last_n = df.tail(batch_size)
    middle_n = df.iloc[batch_size:-batch_size].sample(n=batch_size)
    batch_df = pd.concat([first_n, middle_n, last_n]).sort_values(by='week_start_date').reset_index(drop=True)
    logging.debug(f"<= Returning {len(batch_df)} weeks.")

    return batch_df

# start_date, end_date | datetime, event_list | list[Event] => events | list[Event]
def get_events_in_range(event_list: List[Event], start_date: datetime, end_date: datetime = None, week_limit = 52) -> List[Event]:
    """
    Returns all events that may occur within the given date range.
    Default implementation: Filters events in memory.
    Should be overridden in ORM-based implementations for better performance.
    """
    if end_date is None:
        end_date = start_date + timedelta(weeks=week_limit)  # Default max 1-year range if no end date
        logging.debug(f"! No end_date specified, using {end_date.strftime('%Y-%m-%d')} ({week_limit} weeks from start_date)")

    logging.debug(f"=> Getting events for {start_date.strftime('%Y-%b-%d')} to {end_date.strftime('%Y-%b-%d')}")

    # Debug
    for event in event_list:
        logging.debug(f"\nChecking {event.name}")

        if event.start_date <= end_date:
            logging.debug(f"1 | Met: {event.start_date.strftime('%Y-%m-%d')} <=  {end_date.strftime('%Y-%m-%d')}")
        else:
            logging.debug(f"1 | Not Met: {event.start_date.strftime('%Y-%m-%d')} >  {end_date.strftime('%Y-%m-%d')}")

        event_end_date = event.end_date.strftime('%Y-%m-%d') if event.end_date is not None else None

        if event.end_date is None or event.end_date >= start_date:

            logging.debug(f"2 | Met:{event_end_date} is none or >= {start_date.strftime('%Y-%m-%d')}")
        else:
            logging.debug(f"2 | Not Met:{event_end_date} is < {start_date.strftime('%Y-%m-%d')}")

    events =  [
        event for event in event_list
        if event.occurs_on_range(start_date,end_date)
    ]

    logging.debug(f"<= Returning {len(events)} events.")

    return events

def count_weekly_events(event_param,existing_events):
    start_date = event_param["start_date"]
    end_date = event_param.get("end_date", None)

    relevant_weeks = get_event_weeks(event_param)
    relevant_events = get_events_in_range(
        event_list= existing_events,
        start_date= start_date,
        end_date= end_date
    )

    weekly_count = {}
    for week_date in relevant_weeks:
        week_start = week_date - timedelta(days=week_date.weekday())
        week_end = week_date + timedelta(days=6)
        week_count = 0

        for date in pd.date_range(start=week_start, end=week_end):
            for event in relevant_events:
                week_count += 1 if event.occurs_on(date) else 0

        weekly_count[week_date] = week_count

    return weekly_count





