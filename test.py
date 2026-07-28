from notestoreclass import NoteStore
from note_operations import load_notes,add_note_flexible,save_notes,search_notes,delete_notes_by_id
from dataclass import Note

raw_notes = load_notes()
store = NoteStore([Note.from_dict(d) for d in raw_notes])

print(store.notes)