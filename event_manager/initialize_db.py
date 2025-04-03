from .event import Base
from .db_session import engine

def initialize_database():
    Base.metadata.create_all(engine)
