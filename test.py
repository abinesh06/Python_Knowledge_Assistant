"""
Quick manual test for NoteStore.add() writing to SQLite.
Run this directly: python test_add.py
"""
from pka.note_store_class import NoteStore
from pka.db import Session
from pka.models import NoteModel
from pka.exceptions import DuplicateNoteError, NoteNotFoundError

store = NoteStore()

print("\n--- Test 16: search_notes() substring match ---")
results = store.search_notes("work")
print(f"Results: {[n.title for n in results]}")

print("\n--- Test 17: search_notes() no match ---")
results2 = store.search_notes("zzz_nomatch")
print(f"Results (should be empty): {results2}")