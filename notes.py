from collections import UserDict
from datetime import datetime
from types import GeneratorType
from itertools import islice

class NoteRecord():
    def __init__(self, mtag, note):
        self.note = note
        self.main_tag = mtag
        self.tags = [mtag]
        self.create_date = datetime.now().date()
        self.change_date = None
        
    def add_tags(self, tags):
        for i in tags:
            self.tags.append(i)
            
    def edit_note(self, new_note):
        self.note = new_note
        
    def __str__(self):
        return f" Main tag: {self.main_tag}\n Tags: {', '.join(self.tags)}\n Note: {self.note}\n Date of creation: {self.create_date}."
        
        
class NoteBook(UserDict):
    def add_record(self, record: NoteRecord) -> None:
        self.data[record.main_tag] = record
        
    def find_note(self, key):
        record = self.data.get(key)
        if record:
            return record
        else:
            raise KeyError
        
    def search_note(self, key: str) -> list:
        notes = []
        for i in self.data.values():
            if key in i.note:
                notes.append(i)
        return notes
                
    def delete_note(self, key: str) -> None:
        if key in self.data:
            self.data.pop(key)
            
    def iterator(self, n=2) -> GeneratorType:
        for i in range(0, len(self), n):
            yield islice(self.data.values(), i, i+n)
                
    
if __name__ == "__main__":
    book = NoteBook()
    fnote = NoteRecord("First", "My first note")
    fnote.add_tags(["today", "bd", "dont forget"])
    book.add_record(fnote)
    snote = NoteRecord("Second", "This is second note")
    snote.add_tags(["test", "help"])
    book.add_record(snote)
    
    