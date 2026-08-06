"""
Scratch/test file for trying out NoteStore.paginated_notes().
This does NOT touch data/notes.json — we build sample notes in memory only.
"""

from pka import NoteStore, Note

# 1. Create a fresh, empty NoteStore — no loading from the real notes.json.
#    This keeps our test data isolated from your actual project notes.
store = NoteStore()

# 2. Manually add some dummy notes directly into memory for testing.
#    Adjust this loop to match whatever your NoteStore.add() signature actually is —
#    e.g. store.add(title=..., content=..., tags=...)
for i in range(1, 11):  # creates 10 dummy notes
    store.add(title=f"Note {i}", text=f"This is the content of note {i}")

# 3. Confirm we actually have 10 notes loaded before testing pagination.
print(f"Total notes loaded: {len(store.notes)}")
print("-" * 40)

# 4. Loop over the generator directly using enumerate().
#    enumerate(iterable, start=1) gives us (page_number, page) pairs,
#    starting the count at 1 instead of the default 0 — just for nicer display.
for page_num, page in enumerate(store.paginated_notes(page_size=3), start=1):
    print(f"--- Page {page_num} ---")
    for note in page:
        print(note)
    print()  # blank line between pages for readability
