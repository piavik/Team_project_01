from collections import UserList
from datetime import datetime
import pickle
from .constants import *
# from .fields import Field


# class Note(Field):
#     ''' Клас для зберігання нотатка. '''
#     @property
#     def value(self) -> str:
#         return self.__value
    
#     @value.setter
#     def value(self, value) -> None:
#         self.__value = value

# class Tags(Field):
#     ''' Клас для зберігання тегів. '''
#     @property
#     def value(self):
#         return self.__value

#     @value.setter
#     def value(self, value) -> None:
#         self.__value = value

class NoteRecord():
    '''
    Клас для зберігання однієї нотатки 
    Відповідає за логіку додавання/видалення/редагування полів note та tags
    '''
    def __init__(self, note: str) -> None:
        self.note = note
        self.tags = []
        self.create_date = datetime.now().date()
        self.change_date = None

    def add_tags(self, tags: list) -> None:
        for i in tags:
            self.tags.append(i.lower())

    def del_tags(self, tags_to_del: list) -> None:
        for i in tags_to_del:
            if i in self.tags:
                self.tags.remove(i)

    def edit_note(self, new_note: str) -> None:
        self.note = new_note

    def __str__(self):
        return (
            f"{BLUE}Tags:{RESET} {', '.join(self.tags)}\n"
            f"{BLUE}Note:{RESET} {self.note}\n"
            f"{BLUE}Date of creation:{RESET} {self.create_date}.\n"
        )

class Notes(UserList):
    ''' Клас для зберігання та управління нотатками. '''    

    def add(self, record: NoteRecord, *args) -> None:
        ''' Додавання запису до self.data '''
        self.data.append(record)

    # key -> NoteRecord
    def delete(self, key, *args) -> None:
        ''' Видалення записів за ключем'''
        self.data.remove(key)

    def load(self, filename=NOTES_NILENAME) -> None:
        ''' load saved data from bin file with pickle '''
        try:
            with open(filename, 'rb') as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print(f'{BLUE}File not found, using new book.{RESET}')

    def save(self, filename=NOTES_NILENAME) -> None:
        ''' save data to bin file with pickle '''
        with open(filename, 'wb') as fh:
            pickle.dump(self.data, fh)


    def find_by_tag(self, tag: str, *args) -> list:
        ''' Пошук записів за тегом '''
        # TODO: returm generator, not list
        notes = []
        for i in self.data:
            if tag.lower() in i.tags:
                notes.append(i)
        return notes
        
    def find_by_note(self, phrase: str, *args) -> list:
        ''' Пошук записів за текстом '''
        # TODO: returm generator, not list
        notes = []
        for i in self.data:
            if phrase in i.note:
                notes.append(i)
        return notes

    # def sort_notes(self, *args) -> list:
    #     lst = []
    #     notes_lst.sort(key = lambda x: len(x.tags), reverse=True)
    #     for i in notes_lst:
    #         lst.append(i)
    #     return lst


if __name__ == "__main__":
    ...
