from note_operations import load_notes,add_note_flexible,save_notes,search_notes,delete_notes_by_id
from exceptions import NoteNotFoundError, NoteError, DuplicateNoteError



def print_menu() -> None:
    """Display the main menu options."""
    print("\n--- Personal Knowledge Assistant ---")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Delete note")
    print("5. Exit")


def main():
    notes=load_notes()

    while True:

        print_menu()

        choice=input("Choose Option (1-5): ").strip()

        if choice=="1":
            title=input("Title: ").strip()
            text=input("Text: ").strip()

            try:
                added_notes=add_note_flexible(notes,title,text)
                save_notes(added_notes)
                print("Notes Added")

            except  NoteError as e:
                print(f"Error: {e}")
            
        
        elif choice=="2":
            print("Please find the List of Notes")
            print(notes)

        elif choice=="3":
            keyword=input("Enter the Keyword: ").strip()
            search_result=search_notes(keyword,notes)
            print("Please find the Search Result")
            print(search_result)

        elif choice=="4":
            note_id=input("Enter the Note ID: ").strip()
            try:
             delete_result=delete_notes_by_id(int(note_id),notes)
             save_notes(delete_result)
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



