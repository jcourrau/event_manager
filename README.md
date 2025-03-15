# Event Manager

## Overview

The event Manager is a Python module designed to handle recurring events efficiently. It provides a robust system for managing events with **weekly** and **monthly** recurrence, allowing users to track and count events over time. This is particularly useful for financial tracking, scheduling, and automation tools.

## Features

- **Recurring Events:** Supports `weekly` and `monthly` recurrence patterns.
- **Date Range Filtering:** Retrieve events occurring in a specific period.
- **Event Counting:** Count occurrences of events within a time frame.
- **Efficient Performance:** Optimized for handling large datasets.
- **Comprehensive Testing:** Includes unit tests to validate calculations.

## Installation

Clone this repository and install the dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Importing the Module

```python
from event_manager import Event
```

### Creating an Event
Weekly event:
```python
from datetime import datetime

# Create a recurring event
event = Event(
    name=" Workout",
    start_date=datetime(2024, 3, 5),
    recurrent_type="weekly",
    days=[2,4]  # Occurs every Wednesday and Friday
)
```
Bi-Weekly event:
```python
from datetime import datetime

# Create a recurring event
event = Event(
    name="Basketball practice",
    start_date=datetime(2024, 3, 5),
    recurrent_type="weekly",
    interval = 2, # Every two weeks
    days=[1]  # On Tuesdays
)
```
Monthly event:
```python
from datetime import datetime

# Create a recurring event
event = Event(
    name="Monthly Payment",
    start_date=datetime(2024, 3, 5),
    recurrent_type="monthly",
    days=[5]  # Occurs on the 5th of every month
)
```

### Retrieving Events in a Date Range

```python
from datetime import datetime

events = [
    Event("Rent Payment", datetime(2024, 3, 1), recurrent_type="monthly", days=[1]),
    Event("Salary", datetime(2024, 3, 1), recurrent_type="monthly", days=[1, 15]),
]

filtered_events = get_events_in_range(events, datetime(2024, 3, 1), datetime(2024, 6, 1))
print(filtered_events)
```

### Counting Weekly Events
Before creating an event, you can check how many events have been creating for 48 relevant weeks by default. 
You can change this by editing the parameter `week_limit=48`
```python
new_event_data = {
    "name": "Team Meeting",
    "start_date": datetime(2024, 3, 1),
    "recurrent_type": "n-weekly",
    "interval": 2,
    "days": [0, 4]  # Mondays and Thursdays
}

weekly_counts = count_weekly_events(new_event_data, events, week_limit=48)
print(weekly_counts)
```

## Class & Function Reference

### `Event` Class

| Method                          | Description                                                  |
|----------------------------------|--------------------------------------------------------------|
| `__init__(...)`                  | Initializes an event with recurrence rules.                 |
| `occurs_on(date)`                | Checks if an event occurs on a given date.                  |
| `get_occurrences(start, end)`     | Retrieves all occurrences within a date range.              |
| `occurs_on_range(start, end)`     | Checks if an event may occur in a given range.              |
| `__str__()`                       | Returns a string representation of the event.               |

### Utility Functions

| Function                                    | Description                                                                    |
|---------------------------------------------|--------------------------------------------------------------------------------|
| `get_event_weeks(event, week_limit=48)`     | Retrieves weeks where an event occurs.                                         |
| `get_events_in_range(events, start, end)`   | Filters events occurring within a given date range.                            |
| `count_weekly_events(event, events)`        | Counts the existing events on the relevant weeks a new event might be created. |

## Running Tests

Run unit tests using `unittest`:

```sh
python -m unittest discover tests
```

## Dependencies

Ensure you have the required dependencies installed:

```
- pandas
- python-dateutil
- pytz
```

## Conclusion

Scheduler is a flexible and efficient module for handling recurring events. It is designed for applications in **finance tracking, scheduling, and automation**. The built-in tests ensure the accuracy and reliability of event calculations.

For further improvements or contributions, feel free to submit a pull request!
