class Note:

    def __init__(self,id,title,text):
       # print("Init calling")
        self.id=id
        self.title=title
        self.text=text

    def __repr__(self):

        return f"Note (Id: {self.id} , Title: {self.title})"

    def __str__(self):
        return f"[{self.id}] {self.title}: {self.text}"
        
    def to_dict(self):
       # print("ToDict calling")
        return {"id":self.id,"title":self.title,"text":self.text}
    
    @classmethod
    def from_dict(cls,data):
       # print("Classmethod calling")
        return cls(data["id"],data["title"],data["text"])
    
#n = Note(1, "Groceries", "milk, eggs")
#print(n)          # uses __str__
#print([n])        # uses __repr__ (inside a list)
#print(repr(n))    # uses __repr__ directly