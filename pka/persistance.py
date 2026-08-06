"""
Atomic file-write utilities for the PKA package.

Wraps JSON persistence so that a crash or error mid-write can never leave
notes.json in a corrupted, half-written state. Writes go to a temp file
first, and only replace the real file once the write completes successfully.
"""

from contextlib import contextmanager
import os
import tempfile


@contextmanager
def safe_write(path):
    """
    Context manager yielding a writable file handle to a temp file.
    On successful exit, atomically replaces `path` with the temp file's
    contents. On exception, discards the temp file and leaves `path`
    untouched.

    Usage:
        with safe_write("data/notes.json") as f:
            json.dump(notes, f, indent=2)
    """
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(path))
    f = os.fdopen(temp_fd, "w")
    #print(temp_fd)
    #print(temp_path)

    try:
        yield f
        f.close()
        os.replace(temp_path, path)
    except Exception:
        f.close()
        os.remove(temp_path)
        raise