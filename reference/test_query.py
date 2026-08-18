# from pka.db import Note, Session

# session = Session()
# notes = session.query(Note).all()

# for n in notes:
#     print(n.id, n.text, n.tags, n.created_at)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pka.models import Base, Document, Chunk

engine = create_engine("sqlite:///data/kb.db", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    doc = session.get(Document, 1)
    for chunk in doc.chunks:
        print(chunk.chunk_index, "->", chunk.content)

    first_chunk = session.get(Chunk, 1)
    print("belongs to:", first_chunk.document.title)