# f=open("data/notes.json","w")
# f.write("Hello Abi")
# f.close()

#with open("data/notes.json","w") as f:
#    f.write("Hello")

import json 
from pathlib import Path 

notes={
    "id":1,
    "title":"AI",
    "text":"AI is an powerfull tool"
}
def write_json_to_file():
    with open("data/notes.json","w") as f:
        json.dump(notes,f)

def load_json_from_file():
    with open("data/notes.json","r") as f:
      return  json.load(f)
    
def dumps_from_file():
    with open("data/notes.json","w") as f:
       return json.dumps(notes)

def load_file_with_safety():
    try:
        with open("data/notes.json") as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return "Error While loading File"

DATA_FILE=Path("data")/"notes.json"

def load_file_with_safety_path():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return "Error While loading File"
    
#ans=write_json_to_file()

ans=load_file_with_safety_path()

print(ans)