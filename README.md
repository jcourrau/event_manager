# Event Manager - Documentation

## Overview

Event Manager is a Python-based module designed to handle recurring events efficiently. It allows users to create, track, and manage events with different recurrence rules such as **weekly**, **bi-weekly**, and **monthly**. The system provides functionality to count and summarize events occurring within a time frame, making it useful for controlling the amount of events created for optimization and scheduling tools.

## Features

- **Recurring Events:** Supports **n-weekly** and **monthly** recurrence.
- **Event Counting:** Retrieves the number of events occurring in a given period.
- **ORM-Friendly Design:** Can be integrated with databases.
- **Optimized Performance:** Uses batch queries to improve efficiency.
- **Flexible Filtering:** Retrieve events by date ranges and recurrence rules.
- **Comprehensive Testing:** Includes various test cases to validate the system.

## Installation

Install dependencies from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Usage

### Importing the Module

```python
from event_recurrance import Event, count_weekly_events, format_weekly_events, summary_weekly_events
```

### Creating an Event

```python
from datetime import datetime

event = Event(
    name="Gym Membership Payment",
    start_date=datetime(2024, 3, 5),
    recurrent_type="monthly",
    days_of_month=[5]
)
```

### Counting Weekly Events

```python
new_event_data = {
    "name": "Test Event",
    "start_date": datetime(2024, 3, 1),
    "recurrent_type": "n-weekly",
    "interval": 2,
    "days_of_week": [0, 4]  # Mondays and Thursdays
}

weekly_counts = count_weekly_events(new_event_data, [event])
format_weekly_events(weekly_counts)
print(summary_weekly_events(weekly_counts))
```

## Functions & Methods

### `Event` Class

| Method                                                                                        | Description                                                      |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `__init__(name, start_date, end_date, recurrent_type, interval, days_of_week, days_of_month)` | Initializes an event with recurrence rules.                      |
| `occurs_on(date)`                                                                             | Checks if an event occurs on a given date.                       |
| `_matches_weekly_interval(date)`                                                              | Validates if an event follows the correct **n-weekly** interval. |
| `__str__()`                                                                                   | Returns a string representation of the event.                    |

### Core Functions

| Function                                                    | Description                                                          |
| ----------------------------------------------------------- | -------------------------------------------------------------------- |
| `get_events_in_range(start_date, end_date, event_queryset)` | Retrieves events occurring within a given date range.                |
| `count_events(start_date, end_date, event_queryset)`        | Counts events in a specific time period.                             |
| `week_range(target_date)`                                   | Returns the Monday and Sunday of a given week.                       |
| `get_event_weeks(event_data, week_limit=42)`                | Retrieves all Mondays of weeks where an event occurs.                |
| `count_weekly_events(new_event_data, event_queryset)`       | Consults the  number of events per week beforewh adding a new event. |
| `format_weekly_events(weekly_event_counts)`                 | Prints weekly event counts in a human-readable format.               |
| `summary_weekly_events(weekly_event_counts)`                | Returns a summary of total and average weekly events.                |

## Sample Event List

`sample_event_list.py` contains predefined recurring events:

```python
existing_events = [
    Event("Rent Payment", datetime(2024, 3, 1), recurrent_type="monthly", days_of_month=[1]),
    Event("Gym Membership", datetime(2024, 3, 5), recurrent_type="monthly", days_of_month=[5]),
    Event("Salary", datetime(2024, 3, 1), recurrent_type="monthly", days_of_month=[1, 15]),
]
```

## Running Test Cases

Run `test_cases.py` to validate event calculations:

```sh
python test_cases.py
```

### Example Test Case

```python
new_event_data = {
    "name": "Weekly Sync",
    "start_date": datetime(2024, 3, 4),
    "recurrent_type": "n-weekly",
    "interval": 1,
    "days_of_week": [0]
}
print("Test Case: Weekly Sync on Mondays")
print(summary_weekly_events(count_weekly_events(new_event_data, existing_events)))
```

## Dependencies

The project requires the following dependencies:

```
- dateutils==0.6.12
- numpy==2.2.3
- openpyxl==3.1.5
- pandas==2.2.3
- python-dateutil==2.9.0.post0
- pytz==2025.1
- six==1.17.0
- tzdata==2025.1
```

## Conclusion

This module is a flexible solution for handling recurring events, particularly useful for **financial tracking, scheduling, and calendar applications**. The provided test cases ensure reliability, while its **modular design** allows easy expansion.
