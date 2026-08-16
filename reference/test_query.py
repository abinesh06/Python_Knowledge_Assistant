from pka.db import Note, Session

session = Session()
notes = session.query(Note).all()

for n in notes:
    print(n.id, n.text, n.tags, n.created_at)