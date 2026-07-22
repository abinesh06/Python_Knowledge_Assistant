class Note:

    def __init__(self,id,title,text):
       # print("Init calling")
        self.id=id
        self.title=title
        self.text=text

    def __repr__(self):

        return f"Note (Id: {self.id} , Title: {self.title})"
    
    def to_dict(self):
       # print("ToDict calling")
        return {"id":self.id,"title":self.title,"text":self.text}
    
    @classmethod
    def from_dict(cls,data):
       # print("Classmethod calling")
        return cls(data["id"],data["title"],data["text"])
    
