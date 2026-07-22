from note import Note

#n=Note(1,"Docker","Docker is a powerful Tool")

#print(n)

#print(n.title)

data = {"id": 2, "title": "Meeting", "text": "Standup at 10am"}
n2 = Note.from_dict(data)
print(n2)
print(n2.to_dict())

