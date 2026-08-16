from datetime import datetime
from pka.db import Note, Session

session = Session()

new_note = Note(
    text="Testing the ORM against my existing notes table 222.",
    tags="work,ideas",
    created_at=datetime.utcnow().isoformat()
)

session.add(new_note)
session.commit()

print(new_note.id)