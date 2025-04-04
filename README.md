# Event Manager

## Overview

**Event Manager** is a modular Python library for managing recurring events using SQLAlchemy.
It is designed to dynamically compute occurrences for `weekly` and `monthly` recurring patterns, making it useful for applications such as **financial tracking**, **subscription scheduling**, and **task automation**.

## Features

- **Flexible Recurrence Rules**: Supports both weekly and monthly recurrences.
- **Database Integration**: Built on top of SQLAlchemy and supports polymorphic inheritance.
- **Transaction Support**: Extended class for financial transactions (income, expenses, savings).
- **Occurrence Generation**: Calculates occurrences dynamically in any date range.
- **Pandas Integration**: Outputs data as DataFrames for reporting and analysis.
- **Reusable Architecture**: Extend the `Event` class with custom subclasses.

## Installation

Install directly from GitHub:
```sh
pip install git+https://github.com/jcourrau/event_manager.git
```

Or clone the repository and install dependencies manually:
```sh
pip install -r requirements.txt
```

## Usage

### Importing the Module

```python
import event_manager as em
```

### Creating Events

Weekly event:
```python
from datetime import datetime

event = em.Event(
    name="Workout",
    start_date=datetime(2024, 3, 5),
    recurrent_type="weekly",
    interval=1,
    days=[2, 4]  # Wednesday and Friday
)
```

Monthly event:
```python
event = em.Event(
    name="Rent",
    start_date=datetime(2024, 3, 1),
    recurrent_type="monthly",
    interval=1,
    days=[1]  # 1st of every month
)
```

### Using the `Transaction` Subclass

```python
from event_manager.event_extensions import Transaction

tx = Transaction(
    name="Gym Membership",
    start_date=datetime(2024, 4, 1),
    recurrent_type="monthly",
    interval=1,
    days=[1],
    amount=30.00,
    transaction_type="expense",
    user_id="your_user_uuid"
)
```

### Saving and Retrieving Events

```python
em.create_event(tx)
events = em.get_user_transactions("your_user_uuid", start, end)
```

### Generating Occurrences

```python
df = em.get_occurrence_df(events, start, end)
print(df)
```

### Updating and Deleting

```python
em.update_event(tx.id, {"amount": 35.00})
em.delete_event(tx.id)
```

## Class & Function Reference

### Event Class

| Method                          | Description                                                  |
|----------------------------------|--------------------------------------------------------------|
| `__init__(...)`                  | Create an event with recurrence logic.                       |
| `occurs_on(date)`                | Returns True if the event occurs on a given date.            |
| `get_occurrences(start, end)`    | Lists all dates the event occurs within a date range.        |
| `occurs_on_range(start, end)`    | Checks if the event falls in a date range.                   |
| `__str__()`                      | Returns a string representation of the event.                |

### Transaction Class

| Attribute/Method            | Description                                                   |
|-----------------------------|---------------------------------------------------------------|
| `amount`                    | Transaction amount (positive float).                          |
| `transaction_type`          | One of: `'income'`, `'expense'`, `'savings'`.                |
| `user_id`                   | Identifier to link transactions to users.                    |
| `__str__()`                 | Outputs the type and name as a string.                       |

### CRUD Functions

| Function                      | Description                                                  |
|-------------------------------|--------------------------------------------------------------|
| `create_event(event)`         | Saves a new event to the database.                          |
| `get_event_by_id(id)`         | Fetches a specific event from the DB.                       |
| `update_event(id, updates)`   | Updates event fields in the DB.                             |
| `delete_event(id)`            | Deletes an event from the DB.                               |

### Utilities

| Function                                | Description                                                      |
|-----------------------------------------|------------------------------------------------------------------|
| `get_event_weeks(event)`                | Returns start dates of weeks with valid occurrences.             |
| `get_events_in_range(events, start, end)` | Filters events active within the date range.                    |
| `count_weekly_events(event, events)`    | Counts how many events happen during the same weeks.            |
| `get_occurrence_df(events, start, end)` | Returns all occurrences in a `pandas.DataFrame`.                |

## Example Script: `example_usage.py`

This script demonstrates how to:
- Create and store multiple transactions
- Retrieve them based on a user and date range
- Generate and print their occurrences
- Update specific entries
- Delete one entry
- Refresh the list and regenerate the occurrence DataFrame

It walks through a typical CRUD + analytics lifecycle with recurring financial data.

## Dependencies

Ensure the following packages are installed:

- `sqlalchemy`
- `pandas`
- `python-dateutil`
- `pytz`
- `tzdata`
- `numpy`

## Conclusion

**Event Manager** offers a flexible and powerful foundation for modeling recurring behaviors. Whether you are building a finance tracker, scheduler, or recurring reminder system, this module provides the tools to handle dynamic event generation and analysis.
