def view_notes() -> None:
    """Prints all notes in a readable format."""
    if not notes:
        print("No notes found.")
        return
    for note in notes:
        print(f"[{note['id']}] {note['title']}")
        print(f"    {note['text']}")
        print()

def find_note(note_id: int) -> dict | None:
    """Finds a note by its id. Returns None if not found."""
    for note in notes:
        if note["id"] == note_id:
            return note
    return None

def search_notes(keyword: str) -> list:
    """Returns all notes where the keyword appears in the title or text."""
    keyword_lower = keyword.lower()
    return [
        note for note in notes
        if keyword_lower in note["title"].lower() or keyword_lower in note["text"].lower()
    ]

notes = load_notes()
view_notes()

result = find_note(1)
print(f"\nFound: {result}")

results = search_notes("meeting")
print(f"\nSearch results: {results}")