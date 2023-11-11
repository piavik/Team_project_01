from datetime import datetime
import pickle

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

try:
    notes_lst[0]
except NameError:
    notes_lst = []       

def add_record(record: NoteRecord) -> None:
    notes_lst.append(record)
    
def find_by_tag(key: str) -> list:
    notes = []
    for i in notes_lst:
        if key in i.tags:
            notes.append(i)
    return notes
    
def find_by_note(key: str) -> list:
    notes = []
    for i in notes_lst:
        if key in i.note:
            notes.append(i)
    return notes

def sort_notes():
    lst = []
    notes_lst.sort(key= lambda x: len(x.tags), reverse=True)
    for i in notes_lst:
        lst.append(i)
    return lst       
            
def delete_note(key) -> None:
    notes_lst.remove(key)
    
def save_notes(filename="notes_book.bin"):
    with open(filename, 'wb') as fh:
        pickle.dump(notes_lst, fh)
        
def load_notes(filename="notes_book.bin"):
    global notes_lst
    try:
        with open(filename, 'rb') as fh:
            notes_lst = pickle.load(fh)
    except FileNotFoundError:
        ...
  
if __name__ == "__main__":
    ...
    
    