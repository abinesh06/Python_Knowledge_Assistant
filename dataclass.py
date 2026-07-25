from dataclasses import dataclass, field 
from datetime import datetime


@dataclass
class Note:
    id:int
    title:str 
    text:str 
    tags: list = field(default_factory=list)
    created_on: str = field(default="",init=False)

    def __post_init__(self):
        print("Calling Post Init")
        if not self.created_on:
            self.created_on=datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id":self.id,
            "title": self.title,
            "text": self.text,
            "created_on": self.created_on
        }
    
    @classmethod
    def from_dict(cls,data:dict) -> Note:
        note=cls(
            id=data["id"],
            title=data["title"],
            text=data["text"]
        )

        return note


        
n1=Note(1,"AI","AI is powerfull")
n2=Note(2,"AI 2","AI 2 is powerfull")

n1.tags.append("helo I am a tag")

print(n1)
print(n2)

data = {"id": 2, "title": "Meeting", "text": "Standup at 10am"}
n3 = Note.from_dict(data)
print(n3)