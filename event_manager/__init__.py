"""
Event Manager module for handling recurring events and transactions.
"""

# Base class
from event import Event

# Extensions
from event_extensions import (
    Transaction,
    get_user_transactions
)

# CRUD
from event_crud import (
    create_event,
    update_event,
    delete_event,
    get_event_by_id
)

# Utility functions
from .utils import get_occurrence_df

__all__ = [
    "Event",
    "Transaction",
    "get_user_transactions",
    "create_event",
    "get_event_by_id",
    "update_event",
    "delete_event"
]
