from pka.data_class import Note
from pka.exceptions import DuplicateNoteError, NoteNotFoundError
from pka.text_utills import chunk_text

class NoteStore:
    def __init__(self, notes: list["Note"] = None):
        self.notes: list["Note"] = notes or []


    def add(self,title: str, text: str, tags : list[str]=None ) -> Note :
        if any(n.title.lower() == title.lower() for n in self.notes):
            raise DuplicateNoteError(f"Note with title '{title}' already exists")

        new_id = max((n.id for n in self.notes), default=0) + 1
        n = Note(id=new_id, title=title, text=text, tags=tags or [])
        self.notes.append(n)
        return n

    def search_notes(self,keyword : str) -> Note | None :
        """returns all the matches if the keyword in Title or text"""    
        keyword_lower=keyword.lower()
        return [
            x for x in self.notes 
            if keyword_lower==x.title.lower() or keyword_lower==x.text.lower()

        ]
    
    def _find_by_id(self, note_id: int) -> Note:
        """
        Internal helper: returns the note with the given id.
        Raises NoteNotFoundError if no such note exists.
        """
        note = next((n for n in self.notes if n.id == note_id), None)
        if note is None:
            raise NoteNotFoundError(f"No Notes found with the ID:{note_id}")
        return note

    
    def find(self, title: str) -> Note | None:
        """Returns the first note with an exact title match, or None."""
        title_lower = title.lower()
        for n in self.notes:
            if n.title.lower() == title_lower:
                return n
        return None

    def delete(self, title: str) -> bool:
        """Deletes the note with the given exact title. Returns True if deleted, False if not found."""
        note = self.find(title)
        if note:
            self.notes.remove(note)
            return True
        return False

    def delete_by_id(self, note_id: int) -> None:
        """Deletes the note with the given id. Raises NoteNotFoundError if not found."""
        note = self._find_by_id(note_id)
        if note is None:
            raise NoteNotFoundError(f"No Notes found with the ID:{note_id}")
        self.notes.remove(note)

    def to_list(self) -> list[dict]:
        """Convert all Note objects back into plain dicts, for JSON saving."""
        return [n.to_dict() for n in self.notes]

    def __str__(self):
        return f"[{self.notes}]"

    def get_note_chunks(self, note_id: int, max_chunk_size: int = 200, overlap: int = 1) -> list[str]:
        """
        Retrieve a note by id and return its text split into
        overlapping sentence-based chunks. Raises NoteNotFoundError
        if no note with that id exists.
        """
        note = self._find_by_id(note_id)
        if note is None:
            raise NoteNotFoundError(f"No Notes found with the ID:{note_id}")
        return chunk_text(note.text, max_chunk_size=max_chunk_size, overlap=overlap)

#store = NoteStore()
#store.add(1, "Groceries", "milk, eggs, bread")
#store.add(2, "Workout", "leg day", tags=["fitness"])

#found = store.find("Workout")
#print(found.text)

#missing = store.find("Nonexistent")
#print(missing)

#deleted = store.delete("Groceries")
#print(deleted)
#print(len(store.notes))

#deleted_again = store.delete("Groceries")
#print(deleted_again)  

#store = NoteStore()
#print(store)
#store.add(1,"Groceries", "milk, eggs, bread")
#store.add(2,"Workout", "leg day", tags=["fitness"])
#store.add(3,"Workout", "Arm day", tags=["fitness 2"])
#print(store.notes.tags)
#search=store.search_notes("workout")

#print(search)

#print(store.notes)
#print(len(store.notes))
#print(store.notes[0].title)


#store = NoteStore()
#n1 = store.add(1, "A", "text a",["fitness"])
#n2 = store.add(2, "B", "text b")
#print(n1.tags, n2.tags)
