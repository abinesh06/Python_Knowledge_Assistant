from dataclasses import dataclass,field

@dataclass
class Note:
    title: str
    content: str
    tags: list = field(default_factory=list)
    created_at: str = ""

    def __str__(self):
        return f"[{self.title}] {self.content} (tags: {self.tags})"

n = Note(title="Groceries", content="milk, eggs", tags=["home"])
print(n)

n2 = Note(title="Empty tags test", content="just checking", tags=[])
print(n2)