from typing import Union
from event import Event
from db_session import session_scope

def create_event(event_obj: Event) -> None:
    """Stores a new Event (or subclass) in the database."""
    with session_scope() as session:
        session.add(event_obj)


def get_event_by_id(event_id: int) -> Union[Event, None]:
    """Fetches a single event by its ID."""
    with session_scope() as session:
        return session.query(Event).filter_by(id=event_id).first()


def update_event(event_id: int, updates: dict) -> bool:
    """Updates fields of an event. Returns True if successful."""
    with session_scope() as session:
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            return False
        for key, value in updates.items():
            setattr(event, key, value)
        return True


def delete_event(event_id: int) -> bool:
    """Deletes an event by ID. Returns True if deleted."""
    with session_scope() as session:
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            return False
        session.delete(event)
        return True
