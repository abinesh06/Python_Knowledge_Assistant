notes=[]

def add_notes(title,text,category="General"):
    note={
        "id":len(notes)+1,
        "title":title,
        "text":text,
        "category":category
    }
    notes.append(note)
def add_tags(note, *tags):
    note["tags"] = list(tags)

def add_note_flexible(title,text, **extra_fields):
    note={        
        "id":len(notes)+1,
        "title":title,
        "text":text
        }
    note.update(extra_fields)
    notes.append(note)
    return note
n=add_note_flexible("Trip Plan","Book Flights", priority="High",price="Medium")
print(n)

#add_tags(new_note, "personal", "shopping", "urgent")
#print(new_note["tags"]) 
add_notes("My Title 1","My Text 1 added into my Learning notes")
add_notes("My Title 2","My Text 2 added into my Learning notes","AI")
#add_notes(text="text1, text2") --> This will Error Out
##print(notes)
#for x in notes:
#   print(f"[{x['id']}] {x['title']} {x['text']} {x['category']}")

#print(notes[0]["title"])