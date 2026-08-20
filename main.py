from pka import Note, NoteStore, NoteNotFoundError, NoteError, DuplicateNoteError, summarize_note, ask_note
from anthropic import APIError


def print_menu() -> None:
    """Display the main menu options."""
    print("\n--- Personal Knowledge Assistant ---")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Delete note")
    print("5. Summarize a note")
    print("6. Ask about a note")
    print("7. Exit")


def main():
    store = NoteStore()

    while True:

        print_menu()

        choice=input("Choose Option (1-7): ").strip()

        if choice=="1":
            title=input("Title: ").strip()
            text=input("Text: ").strip()

            try:
                store.add(title=title,text= text)
                #save_notes(store.to_list())
                print("Notes Added")

            except NoteError as e:
                print(f"Error: {e}")


        elif choice=="2":
            print("Please find the List of Notes")

            page_size = 3
            found_any = False

            for page_num, page in enumerate(store.paginated_notes(page_size=page_size), start=1):
                found_any = True
                print(f"\n--- Page {page_num} ---")
                for n in page:
                    print(n)

                see_more = input("\nShow next page? (y/n): ").strip().lower()
                if see_more != "y":
                    break

            if not found_any:
                print("No notes found.")

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
                #save_notes(store.to_list())
                print("Note Deleted")
            except NoteNotFoundError as e:
                print(e)

        elif choice=="5":
            note_id=input("Enter the Note ID to summarize: ").strip()
            try:
                note = store.get_by_id(int(note_id))
                summary = summarize_note(note.text)
                print("\n--- Summary ---")
                print(summary)
            except NoteNotFoundError as e:
                print(e)
            except ValueError as e:
                print(f"Error: {e}")
            except APIError as e:
                print(f"Claude API error: {e}")

        elif choice=="6":
            note_id=input("Enter the Note ID to ask about: ").strip()
            question=input("Your question: ").strip()
            try:
                note = store.get_by_id(int(note_id))
                answer = ask_note(note.text, question)
                print("\n--- Answer ---")
                print(answer)
            except NoteNotFoundError as e:
                print(e)
            except ValueError as e:
                print(f"Error: {e}")
            except APIError as e:
                print(f"Claude API error: {e}")


        
        elif choice=="7":
            print("Goodbye !!!!")
            break

        else:
            print("Invalid Choice - Please Enter 1 - 7")


if __name__=="__main__":
    main()