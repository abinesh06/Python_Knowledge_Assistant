from main import notes 
class NoteError(Exception):
    """Base Exception for all the Note Errors"""
    pass

class NoteNotFoundError(NoteError):
    """Raise an Exception where Given Note ID was not found"""
    pass 

class InvalidNoteError(NoteError):
    """Raise an Exception when invalid data is passed"""
    pass 

def validate_notes(title: str, text : str):
    """Validate the Notes content and raise an exception"""
    if not title or not title.strip():
        raise InvalidNoteError("Title cannot be Empty")
    if not text or not text.strip():
        raise InvalidNoteError("Text Cannot be empty")

#try:
#    validate_notes("hello","")
#except InvalidNoteError as e:
#    print(e)
