from dataclass import Note
class NoteStore:
    def __init__(self):
        self.notes: list["Note"] = []


    def add(self,id : int, title: str, text: str, tags : list[str]=[]) -> Note :
        n=Note(id=id,title=title,text=text,tags=tags or [])
        self.notes.append(n)
        return n

    def search_notes(self,keyword : str) -> Note | None :
        """returns all the matches if the keyword in Title or text"""    
        keyword_lower=keyword.lower()
        return [
            x for x in self.notes 
            if keyword_lower==x.title.lower() or keyword_lower==x.text.lower()

        ]

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

store = NoteStore()
print(store)
#store.add(1,"Groceries", "milk, eggs, bread")
#store.add(2,"Workout", "leg day", tags=["fitness"])
#store.add(3,"Workout", "Arm day", tags=["fitness"])
#print(store.notes)
#search=store.search_notes("workout")

#print(search)

#print(store.notes)
#print(len(store.notes))
#print(store.notes[0].title)
