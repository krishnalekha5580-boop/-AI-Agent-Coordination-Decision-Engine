"""
db/session.py

Database engine and session setup. Uses SQLite for now (zero setup,
single file on disk). To migrate to Postgres later, only DATABASE_URL
needs to change -- models.py and repository.py stay the same.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

# SQLite file will be created at the project root as pm_decision_engine.db
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///pm_decision_engine.db")

# check_same_thread=False is needed for SQLite when used from Streamlit,
# which may access the DB from a different thread than it was created in.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """Create all tables if they don't already exist. Safe to call multiple times."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new database session. Caller is responsible for closing it."""
    return SessionLocal()