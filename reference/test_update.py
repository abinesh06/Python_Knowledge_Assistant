from pka.db import Note, Session

session = Session()

note = session.query(Note).filter(Note.id == 1).first()
print(note.text)   # confirm what it currently says

note.text = "Updated: testing the ORM against my existing notes table."
session.commit()

session2 = Session()
check = session2.query(Note).filter(Note.id == 1).first()
print(check.text)