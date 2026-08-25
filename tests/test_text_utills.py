"""
Tests for pka/text_utils.py

These are the first "real" tests in the project, deliberately targeting
text_utils.py first because every function in it is PURE — input in,
output out, no database, no file system, no network call. That means
zero setup/teardown and 100% deterministic results, which makes it the
easiest possible starting point before we tackle mocking (Day 3) or
DB testing (Day 4).

Run with:  pytest
(from the project root, with the venv active)
"""

from pka.text_utills import extract_hashtags, split_into_sentences, chunk_text


# ---------------------------------------------------------------------------
# extract_hashtags()
# ---------------------------------------------------------------------------

def test_extract_hashtags_basic():
    # Arrange
    text = "Loving the #python journey, feeling #motivated"

    # Act
    result = extract_hashtags(text)

    # Assert
    assert result == ["python", "motivated"]


def test_extract_hashtags_none_present():
    # Arrange — plain text with no '#' anywhere
    text = "Just a normal note with no tags in it"

    # Act
    result = extract_hashtags(text)

    # Assert — re.findall() on no matches returns an empty list, not None
    assert result == []


def test_extract_hashtags_duplicates_are_kept():
    # Arrange — the same tag appears twice
    text = "So much #python today, more #python tomorrow"

    # Act
    result = extract_hashtags(text)

    # Assert — extract_hashtags uses re.findall(), which returns every match
    # in order. It does NOT deduplicate, so both #python hits should appear.
    # If you ever want unique tags, that's a deliberate change to make later
    # (e.g. wrapping the result in set() or dict.fromkeys()) — not a bug.
    assert result == ["python", "python"]


# ---------------------------------------------------------------------------
# split_into_sentences()
# ---------------------------------------------------------------------------

def test_split_into_sentences_basic():
    # Arrange
    text = "Sarah owns backend. Raj owns API. Done by Friday!"

    # Act
    result = split_into_sentences(text)

    # Assert
    assert result == ["Sarah owns backend.", "Raj owns API.", "Done by Friday!"]


def test_split_into_sentences_abbreviation_edge_case():
    # Arrange — "Dr." contains a '.' followed by a space, which is exactly
    # the boundary pattern (?<=[.!?])\s+ looks for. The function has no
    # special-case handling for abbreviations, so it WILL split here —
    # this test documents that real (if slightly wrong-feeling) behavior
    # rather than assuming smarter handling that doesn't exist in the code.
    text = "Dr. Smith arrived early."

    # Act
    result = split_into_sentences(text)

    # Assert
    assert result == ["Dr.", "Smith arrived early."]


# ---------------------------------------------------------------------------
# chunk_text()
# ---------------------------------------------------------------------------
# Note: chunk_text2() exists in text_utils.py but is unused/dead code
# (confirmed with Abi), so it is intentionally NOT tested here.

def test_chunk_text_real_traced_behavior():
    # Arrange
    # NOTE: the docstring's own example claims this call should return
    #   ['Sarah owns backend.', 'Raj owns API.', 'Raj owns API. Done by Friday!']
    # but tracing the actual loop shows that's NOT what the code does.
    # When a sentence overflows max_chunk_size, the function carries the
    # overlap sentence(s) from the chunk that just got flushed AND still
    # appends the triggering sentence to the new chunk — so the new chunk
    # starts with the carried-over sentence(s) PLUS the sentence that
    # caused the overflow, not just the triggering sentence alone.
    # This test locks in the real, current behavior as a baseline.
    # Flag for later: either fix the docstring or fix the logic —
    # don't quietly "fix" this test to match the docstring instead.
    text = "Sarah owns backend. Raj owns API. Done by Friday!"

    # Act
    result = chunk_text(text, max_chunk_size=30)

    # Assert — actual traced output, not the docstring's claimed output
    assert result == [
        "Sarah owns backend.",
        "Sarah owns backend. Raj owns API.",
        "Raj owns API. Done by Friday!",
    ]


def test_chunk_text_short_text_single_chunk():
    # Arrange — text well under max_chunk_size should never be split at all
    text = "Just one short sentence."

    # Act
    result = chunk_text(text, max_chunk_size=200)

    # Assert — one sentence in, one chunk out
    assert result == ["Just one short sentence."]