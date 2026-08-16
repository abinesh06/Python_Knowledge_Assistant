from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    tags = Column(String, nullable=True)
    created_at = Column(String, nullable=False)

    def __repr__(self):
        return f"<Note(id={self.id}, text={self.text!r})>"


engine = create_engine("sqlite:///data/pka.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)