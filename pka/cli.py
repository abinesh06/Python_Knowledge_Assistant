import click
from pka.note_store_class import NoteStore
from pka.exceptions import DuplicateNoteError, NoteNotFoundError
from pka.llm_client import ask_note

@click.group()
def pkassist():
    """Personal Knowledge Assistant CLI."""
    pass


@pkassist.command()
@click.argument("title")
@click.argument("text")
@click.option("--tags", default=None, help="Comma-separated tags, e.g. --tags work,urgent")
def add(title, text, tags):
    """Add a new note. TITLE and TEXT are required."""
    tag_list = tags.split(",") if tags else None
    store = NoteStore()
    try:
        note = store.add(title=title, text=text, tags=tag_list)
        click.echo(f"Added note #{note.id}: {note.title}")
    except DuplicateNoteError as e:
        raise click.ClickException(str(e))


@pkassist.command()
@click.argument("keyword")
@click.option("--limit", default=5, show_default=True, help="Max results to return")
def search(keyword, limit):
    """Search notes by keyword in title or text."""
    store = NoteStore()
    # TODO: search_notes() currently fetches ALL matches, then we slice here.
    # Fine at current scale — move --limit into the SQL query (LIMIT clause)
    # once note volume grows or this gets exposed via FastAPI (Week 10).
    results = store.search_notes(keyword)[:limit]

    if not results:
        click.echo("No notes found.")
        return

    for note in results:
        click.echo(f"#{note.id} {note.title} — tags: {note.tags}")


@pkassist.command()
@click.argument("note_id", type=int)
@click.argument("question")
def ask(note_id, question):
    """Ask a question about a specific note's content."""
    store = NoteStore()
    try:
        note = store.get_by_id(note_id)
    except NoteNotFoundError as e:
        raise click.ClickException(str(e))

    click.echo("Thinking...")
    answer = ask_note(note.text, question)
    click.echo(f"\n{answer}")


@pkassist.command()
@click.argument("note_id", type=int)
def delete(note_id):
    """Delete a note by id (asks for confirmation first)."""
    store = NoteStore()
    try:
        note = store.get_by_id(note_id)
    except NoteNotFoundError as e:
        raise click.ClickException(str(e))

    click.confirm(f"Delete note #{note.id} '{note.title}'?", abort=True)

    store.delete_by_id(note_id)
    click.echo(f"Deleted note #{note.id}.")

if __name__ == "__main__":
    pkassist()