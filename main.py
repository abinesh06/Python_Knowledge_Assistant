from pka import Note, NoteStore, load_notes, save_notes, NoteNotFoundError, NoteError, DuplicateNoteError


def print_menu() -> None:
    """Display the main menu options."""
    print("\n--- Personal Knowledge Assistant ---")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Delete note")
    print("5. Exit")


def main():
    raw_notes = load_notes()
    store = NoteStore([Note.from_dict(d) for d in raw_notes])

    while True:

        print_menu()

        choice=input("Choose Option (1-5): ").strip()

        if choice=="1":
            title=input("Title: ").strip()
            text=input("Text: ").strip()

            try:
                store.add(title=title,text= text)
                save_notes(store.to_list())
                print("Notes Added")

            except NoteError as e:
                print(f"Error: {e}")


        elif choice=="2":
            print("Please find the List of Notes")

            page_size = 3  # how many notes to show per page — adjust as you like
            if not store.notes:
                print("No notes found.")
            else:
                for page_num, page in enumerate(store.paginated_notes(page_size=page_size), start=1):
                    print(f"\n--- Page {page_num} ---")
                    for n in page:
                        print(n)

                    # Ask the user before fetching the NEXT page — this is where the
                    # generator's laziness actually pays off: the next page isn't
                    # computed until the user says yes.
                    see_more = input("\nShow next page? (y/n): ").strip().lower()
                    if see_more != "y":
                        break

        elif choice=="3":
            keyword=input("Enter the Keyword: ").strip()
            search_result=store.search_notes(keyword)
            print("Please find the Search Result")
            for n in search_result:
                print(n)

        elif choice=="4":
            note_id=input("Enter the Note ID: ").strip()
            try:
                store.delete_by_id(int(note_id))
                save_notes(store.to_list())
                print("Note Deleted")
            except NoteNotFoundError as e:
                print(e)


        elif choice=="5":
            print("Goodbye !!!!")
            break

        else:
            print("Invalid Choice - Please Enter 1 - 5")


if __name__=="__main__":
    main()