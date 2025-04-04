from event import Base
from event_extensions import Transaction
from db_session import engine

def initialize_database():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    initialize_database()
