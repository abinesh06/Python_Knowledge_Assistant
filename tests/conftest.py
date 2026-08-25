import uuid
import pytest
from pka.note_store_class import NoteStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pka.models import Base


# @pytest.fixture
# def sample_store():
#     """A NoteStore pre-loaded with two notes, fresh for every test."""
#     store = NoteStore()
#     suffix = uuid.uuid4().hex[:6]
#     store.add(f"Groceries {suffix}", "Buy milk, eggs, and bread", tags=["errand"])
#     store.add(f"PKA Project {suffix}", "Finish the Week 7 testing module", tags=["work"])
#     return store, suffix

@pytest.fixture
def sample_store(db_session_factory):
    """A NoteStore backed by a fresh in-memory DB, pre-loaded with two notes."""
    store = NoteStore(session_factory=db_session_factory)
    store.add("Groceries", "Buy milk, eggs, and bread", tags=["errand"])
    store.add("PKA Project", "Finish the Week 7 testing module", tags=["work"])
    return store

@pytest.fixture
def db_session_factory():
    """A fresh in-memory SQLite session factory, isolated per test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()