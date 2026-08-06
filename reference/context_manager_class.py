"""
Reference implementation: class-based context manager for atomic file writes.

This is kept for comparison against the @contextmanager (generator-based)
version actually used in pka/persistence.py. Not imported by the live app —
this file exists purely to document the __enter__/__exit__ protocol as an
alternative to the decorator-based approach.

See: pka/persistence.py for the version actually wired into NoteStore.
"""

import json
import os
import tempfile


class SafeWrite:
    """
    Context manager that writes to a temp file first, then atomically
    replaces the target file — so a crash mid-write never corrupts the
    real file.

    Usage:
        with SafeWrite("data/notes.json") as f:
            json.dump(notes, f, indent=2)
    """

    def __init__(self, path):
        self.path = path
        self.temp_path = None
        self.file = None

    def __enter__(self):
        # Create the temp file in the SAME directory as the target.
        # os.replace() is only guaranteed atomic when source and
        # destination live on the same filesystem.
        temp_fd, self.temp_path = tempfile.mkstemp(
            dir=os.path.dirname(self.path)
        )
        self.file = os.fdopen(temp_fd, "w")
        return self.file  # this becomes the value bound by `as f`

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

        if exc_type is None:
            # No exception in the `with` block — the write succeeded.
            # Promote the temp file to be the real file, atomically.
            os.replace(self.temp_path, self.path)
        else:
            # Something went wrong inside the `with` block.
            # Discard the temp file, leave the real file untouched.
            os.remove(self.temp_path)

        return False  # False = don't suppress the exception, let it propagate