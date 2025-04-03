from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DATABASE_URL = "sqlite:///events.db"
engine = create_engine(DATABASE_URL, echo=False)  # echo=True to see queries
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Returns a session ready to be used."""
    return SessionLocal()

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()