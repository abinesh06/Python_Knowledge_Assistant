# pka/models.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NoteModel(Base):
    """
    SQLAlchemy table mapping for a Note.
    Mirrors pka.data_class.Note field-for-field:
      - tags is stored as a comma-separated string (SQLite has no native list type)
      - created_on is stored as a string, matching Note.created_on's isoformat() string
        (not a DateTime column) so no type conversion is needed when moving
        data between the dataclass and the DB row.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    text = Column(Text, nullable=False)
    tags = Column(String, nullable=True)        # e.g. "fitness,leg-day"
    created_on = Column(String, nullable=False)  # isoformat string, e.g. "2026-08-18T10:30:00"

    def __repr__(self):
        return f"<NoteModel(id={self.id}, title={self.title!r})>"