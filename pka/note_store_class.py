from pka.data_class import Note
from pka.exceptions import DuplicateNoteError, NoteNotFoundError
from pka.text_utills import chunk_text
from pka.decorators import log_calls, timed
from pka.models import NoteModel
from pka.db import Session
from datetime import datetime  # add this import at the top

class NoteStore:
    def __init__(self):
        pass



    @log_calls(level="DEBUG")
    def add(self, title: str, text: str, tags: list[str] = None) -> Note:
        session = Session()
        try:
            existing = (
                session.query(NoteModel)
                .filter(NoteModel.title.ilike(title))
                .first()
            )
            if existing is not None:
                raise DuplicateNoteError(f"Note with title '{title}' already exists")

            tags_str = ",".join(tags) if tags else None
            created_on = datetime.now().isoformat()

            note_row = NoteModel(
                title=title,
                text=text,
                tags=tags_str,
                created_on=created_on,
            )
            session.add(note_row)
            session.commit()

            return Note(
                id=note_row.id,
                title=note_row.title,
                text=note_row.text,
                tags=tags or [],
            )

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    
    @log_calls(level="INFO")
    @timed
    def search_notes(self, keyword: str) -> list[Note]:
        """Returns all notes where the keyword appears anywhere in Title or Text."""
        session = Session()
        try:
            pattern = f"%{keyword}%"
            rows = (
                session.query(NoteModel)
                .filter(
                    (NoteModel.title.ilike(pattern)) |
                    (NoteModel.text.ilike(pattern))
                )
                .all()
            )

            return [
                Note(
                    id=row.id,
                    title=row.title,
                    text=row.text,
                    tags=row.tags.split(",") if row.tags else [],
                )
                for row in rows
            ]
        finally:
            session.close()

    @log_calls(level="DEBUG")
    def _find_by_id(self, note_id: int) -> Note:
        """
        Internal helper: returns the note with the given id.
        Raises NoteNotFoundError if no such note exists.
        """
        session = Session()
        try:
            row = session.get(NoteModel, note_id)
            if row is None:
                raise NoteNotFoundError(f"No Notes found with the ID:{note_id}")

            tags_list = row.tags.split(",") if row.tags else []
            return Note(
                id=row.id,
                title=row.title,
                text=row.text,
                tags=tags_list,
            )
        finally:
            session.close()

    @log_calls(level="INFO")
    def find(self, title: str) -> Note | None:
        """Returns the first note with an exact title match, or None."""
        session = Session()
        try:
            row = (
                session.query(NoteModel)
                .filter(NoteModel.title.ilike(title))
                .first()
            )
            if row is None:
                return None

            tags_list = row.tags.split(",") if row.tags else []
            return Note(
                id=row.id,
                title=row.title,
                text=row.text,
                tags=tags_list,
            )
        finally:
            session.close()

    @log_calls(level="DEBUG")
    def delete(self, title: str) -> bool:
        """Deletes the note with the given exact title. Returns True if deleted, False if not found."""
        session = Session()
        try:
            row = (
                session.query(NoteModel)
                .filter(NoteModel.title.ilike(title))
                .first()
            )
            if row is None:
                return False

            session.delete(row)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @log_calls(level="DEBUG")
    def delete_by_id(self, note_id: int) -> None:
        """Deletes the note with the given id. Raises NoteNotFoundError if not found."""
        session = Session()
        try:
            row = session.get(NoteModel, note_id)
            if row is None:
                raise NoteNotFoundError(f"No Notes found with the ID:{note_id}")

            session.delete(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

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

    def paginated_notes(self, page_size: int = 3):
        """
        The generator way: yields ONE page at a time, computed on demand.
        """
        session = Session()
        try:
            offset = 0
            while True:
                rows = (
                    session.query(NoteModel)
                    .order_by(NoteModel.id)
                    .limit(page_size)
                    .offset(offset)
                    .all()
                )
                if not rows:
                    break

                page = [
                    Note(
                        id=row.id,
                        title=row.title,
                        text=row.text,
                        tags=row.tags.split(",") if row.tags else [],
                    )
                    for row in rows
                ]
                yield page

                offset += page_size
        finally:
            session.close()



    @log_calls(level="DEBUG")
    def get_by_id(self, note_id: int) -> Note:
        """Public lookup: returns the note with the given id.
        Raises NoteNotFoundError if no such note exists."""
        return self._find_by_id(note_id)

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
