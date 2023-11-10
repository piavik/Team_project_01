from datetime import datetime
from types import GeneratorType
from itertools import islice

class NoteRecord():
    def __init__(self, note: str) -> None:
        self.note = note
        self.tags = []
        self.create_date = datetime.now().date()
        self.change_date = None
        
    def add_tags(self, tags: list) -> None:
        for i in tags:
            self.tags.append(i)
            
    def edit_note(self, new_note: str) -> None:
        self.note = new_note
        
    def __str__(self):
        return f" Tags: {', '.join(self.tags)}\n Note: {self.note}\n Date of creation: {self.create_date}."
        
notes_lst = []       

def add_record(self, record: NoteRecord) -> None:
    notes_lst.append(record)
    
def find_note_by_tag(self, key: str) -> list:
    notes = []
    for i in self.data.values():
        if key in i.tags:
            notes.append(i)
    return notes
    
def search_note_by_note(self, key: str) -> list:
    notes = []
    for i in self.data.values():
        if key in i.note:
            notes.append(i)
    return notes
            
# def delete_note(self, key: str) -> None:
#     if key in self.data:
#         self.data.pop(key)
        
# def iterator(self, n=2) -> GeneratorType:
#     for i in range(0, len(self), n):
#         yield islice(self.data.values(), i, i+n)
                
    
if __name__ == "__main__":
    ...
    
    