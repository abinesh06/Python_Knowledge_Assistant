# pka/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pka.models import Base

# Single engine, single Base (imported from models.py — not redefined here).
# echo=True prints every SQL statement SQLAlchemy runs, useful while learning;
# we'll likely turn this off once Day 4/5 testing is done.
engine = create_engine("sqlite:///data/pka.db", echo=False)

# Creates the `notes` table if it doesn't exist yet. Safe to call every run —
# it's a no-op if the table's already there.
Base.metadata.create_all(engine)

# Session is a *factory* — calling Session() gives you a new session bound
# to this engine. NoteStore's methods will call Session() each time they
# need to talk to the DB (today's scope — one session per method call).
Session = sessionmaker(bind=engine)