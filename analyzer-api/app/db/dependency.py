# app/db/dependency.py

from app.db.session import DatabaseSession


def get_db():
    """
    Dependency that provides a DatabaseSession using connection pool.
    Automatically returns the connection back to the pool.
    """
    with DatabaseSession() as db:
        yield db
