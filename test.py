from pka import NoteStore

# Create a fresh store and add a note with several sentences
store = NoteStore()
store.add(
    title="Sprint Planning",
    text="Sarah owns backend. Raj owns API integration. We ship by Friday. QA starts Monday. Retro is next Wednesday.",
    tags=["work", "sprint"]
)

# The note we just added should have id=1 (first note, since max() on empty list defaults to 0, +1)
chunks = store.get_note_chunks(note_id=1, max_chunk_size=40, overlap=1)

for i, c in enumerate(chunks):
    print(f"Chunk {i}: {c!r}")

# Also confirm the error path — asking for a note id that doesn't exist
print("\n--- Testing error case ---")
try:
    store.get_note_chunks(note_id=99)
except Exception as e:
    print(f"Caught expected error: {type(e).__name__}: {e}")