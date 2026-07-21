import json
from pathlib import Path
from exceptions import NoteNotFoundError

NOTES_FILE = Path("data/notes.json")

def load_notes() -> list :
    """Load Notes from the JSOn File"""
    try:
     with open(NOTES_FILE,"r") as f:
       return json.load(f)
    
    except (FileNotFoundError,json.JSONDecodeError):
      return []

def save_notes(notes:list) -> None:
  
    with open(NOTES_FILE,"w") as f:
       json.dump(notes,f,indent=2)


def delete_notes_by_id(noteId: int) -> None:
    """Delete the Notes by it's Id"""
    notes=load_notes()

    try:
       delete_note=next(n for n in notes if n["id"]==noteId)
    
    except StopIteration:
       raise NoteNotFoundError(f"No Notes found with the ID:{noteId}")
    
    else:
       notes.remove(delete_note)
       save_notes(notes)
       print(f"Notes Deleted with the ID:{noteId}")

    finally:
       print("Notes Deletion process closed")

    #return delete_note

notes={
    "id":3,
    "title":"AI",
    "text":"AI is an powerfull tool"
}     

try:
   delete_notes_by_id(3)
except NoteNotFoundError as e:
   print(e)
#save_notes(notes)


