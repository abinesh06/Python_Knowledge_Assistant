import json
from pathlib import Path

DATA_FILE = Path("data") / "notes.json"

notes = []

def add_note(title: str, text: str) -> dict:
    """Creates a new note and appends it to the notes list."""
    note = {"id": len(notes) + 1, "title": title, "text": text}
    notes.append(note)
    return note

def save_notes(notes: list) -> None:
    """Saves the notes list to a JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

def load_notes() -> list:
    """Loads notes from the JSON file, or returns an empty list if it doesn't exist."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- Test it ---
notes = load_notes()          # load whatever exists (empty list on first run)
add_note("Groceries", "Milk, eggs, bread")
add_note("Meeting Notes", "Discuss Q3 roadmap")
save_notes(notes)

print("Saved! Current notes:")
for note in notes:
    print(f"[{note['id']}] {note['title']}: {note['text']}")