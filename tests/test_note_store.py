import pytest
from pka.exceptions import DuplicateNoteError, NoteNotFoundError

def test_search_finds_note(sample_store):
    results = sample_store.search_notes("Groceries")
    assert len(results) == 1
    assert "milk" in results[0].text.lower()


def test_delete_removes_note(sample_store):
    title = "Groceries"

    deleted = sample_store.delete(title)
    assert deleted is True

    remaining = sample_store.search_notes(title)
    assert len(remaining) == 0


def test_find_returns_note(sample_store):
    result = sample_store.find("Groceries")
    assert result is not None
    assert result.title == "Groceries"


def test_find_returns_none_when_not_found(sample_store):
    result = sample_store.find("Nonexistent Note")
    assert result is None


def test_find_is_case_insensitive_not_partial(sample_store):
    # ilike() is case-insensitive, so different casing should still match
    result = sample_store.find("groceries")
    assert result is not None
    assert result.title == "Groceries"

    # but there's no wildcard in find()'s query, so a partial title should NOT match
    result_partial = sample_store.find("Grocer")
    assert result_partial is None

def test_add_raises_on_duplicate_title(sample_store):
    with pytest.raises(DuplicateNoteError) as exc_info:
        sample_store.add("Groceries", "some other text")
    assert "Groceries" in str(exc_info.value)

def test_delete_by_id_raises_when_not_found(sample_store):
    with pytest.raises(NoteNotFoundError):
        sample_store.delete_by_id(99999)

def test_delete_returns_false_when_not_found(sample_store):
    result = sample_store.delete("Nonexistent Note")
    assert result is False