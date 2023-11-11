from collections import UserDict
from datetime import datetime
from types import GeneratorType
from itertools import islice
import pickle
from fields import Field, Name, Phone, Birthday, Adress, Email


RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"
FILENAME = "book.dat"

class Record:
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. 
    Відповідає за логіку додавання/видалення/редагування полів та зберігання поля Name
    '''

    def __init__(self, name: str, birthday=None, email=None, adress=None) -> None:
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)
        if adress:
            self.adress = Adress(adress)
        self.emails = []

    def __str__(self) -> str:
        if hasattr(self, 'birthday') and hasattr(self, 'emails') and hasattr(self, 'adress'):
            __days_to_bdy = f"{self.days_to_birthday} days to next birthday" if self.days_to_birthday else f'it is TODAY!'
            __last_part = f"Birthday: {self.birthday}\n{__days_to_bdy}\nEmail: {', '.join(e.value for e in self.emails)}\nAdress: {self.adress}"
        elif hasattr(self, 'birthday') and hasattr(self, 'emails'):
            __days_to_bdy = f"{self.days_to_birthday} days to next birthday" if self.days_to_birthday else f'it is TODAY!'
            __last_part = f"Birthday: {self.birthday}\n{__days_to_bdy}\nEmail: {', '.join(e.value for e in self.emails)}"
        elif hasattr(self, 'birthday') and hasattr(self, 'adress'):
            __days_to_bdy = f"{self.days_to_birthday} days to next birthday" if self.days_to_birthday else f'it is TODAY!'
            __last_part = f"Birthday: {self.birthday}\n{__days_to_bdy}\nAdress: {self.adress}"
        elif hasattr(self, 'birthday'):
            __days_to_bdy = f"{self.days_to_birthday} days to next birthday" if self.days_to_birthday else f'it is TODAY!'
            __last_part = f"Birthday: {self.birthday}\n{__days_to_bdy}"
        elif hasattr(self, 'emails') and hasattr(self, 'adress'):
            __last_part = f"Email: {', '.join(e.value for e in self.emails)}\nAdress: {self.adress}"
        elif hasattr(self, 'adress'):
            __last_part = f"Adress: {self.adress}"
        elif hasattr(self, 'emails'):
            __last_part = f"Email:{', '.join(e.value for e in self.emails)}"
        else:
            __last_part = ""
        message = (
                f"Name: {self.name.value}\n"
                f"Phones: {', '.join(p.value for p in self.phones)}\n"
                f"{__last_part}\n"
            )
        return message

    def add_phone(self, phone: str) -> None:
        ''' Додавання номеру телефону до контакту '''
        if phone not in (ph.value for ph in self.phones):
            self.phones.append(Phone(phone))

    def remove_phone(self, removing: str) -> None:
        ''' Видалення телефону контакта '''
        for phone in self.phones:
            if phone.value == removing:
                self.phones.remove(phone)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        ''' Редагування телефону контакта '''
        if old_phone not in (ph.value for ph in self.phones):
            raise ValueError
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index].value = new_phone

    def find_phone(self, search: str) -> Phone:
        # -> Phone, not str !!!
        ''' Пошук телефону контакта '''
        for phone in self.phones:
            if phone.value == search:
                return phone
        return None

    def add_birthday(self, birthday: str) -> None:
        ''' Додавання дня народження до контакту '''
        self.birthday = Birthday(birthday)

    def add_adress(self, adress: str) -> None:
        ''' Додавання адреси до контакту '''
        self.adress = adress

    def add_email(self, email: str) -> None:
        ''' Додавання email до контакту '''
        if email not in (e.value for e in self.emails):
            self.emails.append(Email(email))


    @property
    def days_to_birthday(self) -> int:
        ''' Кількість днів до наступного дня народження '''
        today = datetime.now().date()
        this_year_birthday = self.birthday.value.replace(year=today.year)
        next_year_birthday = self.birthday.value.replace(year=today.year+1)
        difference = (this_year_birthday - today).days
        if difference <= 0:
            difference = (next_year_birthday - today).days
        return difference

class AddressBook(UserDict):
    ''' Клас для зберігання та управління записами. '''

    def add_record(self, record: Record) -> None:
        '''
        Додавання запису до self.data.
        '''
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        '''
        Пошук записів за іменем.
        '''
        record = self.data.get(name)
        # return record if record else None
        if record:
            return record
        else:
            raise KeyError

    def delete(self, name: str) -> None:
        ''' Видалення записів за іменем. '''
        if name in self.data:
            self.data.pop(name)

    def iterator(self, n=2) -> GeneratorType:
        ''' generator '''
        for i in range(0, len(self), n):
            yield islice(self.data.values(), i, i+n)

    def save(self, filename="book.dat", format='bin'):
        ''' TODO: format selection and using different formats '''
        with open(filename, 'wb') as fh:
            pickle.dump(self.data, fh)

    def load(self, filename="book.dat", format='bin'):
        ''' TODO: format selection and using different formats '''
        # check if filename provided as non-default argument, else -> request, if empty -> set default
        try:
            with open(filename, 'rb') as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print(BLUE + "File not found, using new book." + RESET)
