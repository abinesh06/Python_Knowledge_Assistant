notes=[
     {
    "id":1,
    "title":"AI",
    "text":"AI is an powerfull"
},
     {
    "id":2,
    "title":"AI 2",
    "text":"AI2 is an powerfull tool"
}
]

def print_notes():
    if not notes:
        print("No Notes Found")
        return
    #for note in notes:
        #print(f"[{note['id']}] {note['title']} {note['text']}")
    #notes.append()
    for x in notes:
         print(f"[{x['id']}] {x['title']} {x['text']}")
    for myIndex,myValue in enumerate(notes):
         print(f"Index: {myIndex}, Value : {myValue['title']}")
match_ans=[x for x in notes if x['id']==1]

def search_notes(keyword : str ) -> List | None :
     """returns all the matches if the keyword in Title or text"""
     keyword_lower=keyword.lower()
     return [
          note for note in notes
          if keyword_lower in note["title"].lower() or keyword_lower in note["text"] 
     ]
notes_by_id={note["id"]:note for note in notes} 
#This is a huge performance pattern (O(1) lookup vs O(n) search)

any_note_exists=any(note["id"]==1 for note in notes)
print(any_note_exists)

search_result=search_notes("Tool")

#print(notes_by_id)
#print(notes_by_id[2])

