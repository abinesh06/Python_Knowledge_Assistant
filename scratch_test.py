from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pka.models import Base, Document, Chunk

engine = create_engine("sqlite:///data/kb.db", echo=True)
Base.metadata.create_all(engine)


with Session(engine) as session:
    doc = Document(
        title="Week 5 Notes",
        content="SQLAlchemy is an ORM. It maps classes to tables. Sessions manage units of work.",
        tags="sql,week5",
    )
    doc.chunks.append(Chunk(chunk_index=0, content="SQLAlchemy is an ORM."))
    doc.chunks.append(Chunk(chunk_index=1, content="It maps classes to tables."))
    doc.chunks.append(Chunk(chunk_index=2, content="Sessions manage units of work."))

    session.add(doc)
    session.commit()
    print(f"Saved document id={doc.id} with {len(doc.chunks)} chunks")