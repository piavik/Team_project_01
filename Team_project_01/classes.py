from collections import UserDict, UserList
from datetime import datetime
from types import GeneratorType
from itertools import islice
import pickle
from Team_project_01.fields import *
from Team_project_01.constants import *
from Team_project_01.folder_sort import folder_sort

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
        #перевіряємо чи є у контакта 'birthday'
        if hasattr(self, 'birthday'):
            __days_to_bdy = f"{self.days_to_birthday} days to next birthday" if self.days_to_birthday else f'{GREEN}it is TODAY!{RESET}'
            __last_part = f"{BLUE}Birthday: {RESET}{self.birthday}\n{__days_to_bdy}\n"
        else:
            __last_part = ""
        #перевіряємо чи є у контакта "email", якщо більше одного то пишемо "Emails"
        if self.emails:
            if len(self.emails) > 1:
                __last_part += f"{BLUE}Emails: {RESET}{', '.join(e.value for e in self.emails)}\n"
            elif len(self.emails) == 1:
                __last_part += f"{BLUE}Email: {RESET}{self.emails[0]}\n"
        #перевіряємо чи є у контакта "adress"
        if hasattr(self, "adress") and self.adress != "":
            __last_part += f"{BLUE}Adress: {RESET}{self.adress}"

        message = (
                f"{BLUE}Name: {RESET}{self.name.value}\n"
                f"{BLUE}Phones: {RESET}{', '.join(p.value for p in self.phones)}\n"
                f"{__last_part}"
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

    def change_email(self, old_email:str, new_email:str):
        ''' Редагування email контакта '''
        if old_email not in (e.value for e in self.emails):
            raise KeyError
        for index, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[index].value = new_email

    def delete_email(self, old_email:str):
        ''' Видалення email контакта '''
        for email in self.emails:
            if email.value == old_email:
                self.emails.remove(email)

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
    ''' Клас для зберігання та управління записами адресної книги. '''

    def add_record(self, record: Record) -> None:
        ''' Додавання запису до self.data '''
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        ''' Пошук записів за іменем '''
        record = self.data.get(name)
        # return record if record else None
        if record:
            return record
        else:
            raise KeyError

    def delete(self, name: str) -> None:
        ''' Видалення записів за іменем '''
        if name in self.data:
            self.data.pop(name)

    def iterator(self, n=2) -> GeneratorType:
        ''' generator '''
        try:
            n = int(n)
        except ValueError:
            n = 2
        for i in range(0, len(self), n):
            yield islice(self.data.values(), i, i+n)

    def bd_in_xx_days(self, days: int) -> GeneratorType:
        ''' вертає всі контакти, у яких день народження за {days} днів'''
        suit_lst = []
        for rec in self.data.values():
            if not hasattr(rec, "birthday"):
                continue
            if rec.days_to_birthday < days:
                suit_lst.append(rec)
        if not suit_lst:
            suit_lst.append(f"{BLUE}Noone has birthday in {days} days!{RESET}")
        for i in range(0, len(suit_lst)):
            yield islice(suit_lst, i, i+1)

    def save(self, filename=FILENAME, format='bin') -> None:
        ''' TODO: format selection and using different formats '''
        with open(filename, 'wb') as fh:
            pickle.dump(self.data, fh)

    def load(self, filename=FILENAME, format='bin') -> None:
        ''' TODO: format selection and using different formats '''
        # check if filename provided as non-default argument, else -> request, if empty -> set default
        try:
            with open(filename, 'rb') as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print(f'{BLUE}File not found, using new book.{RESET}')

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

class ErrorHandler():
    ''' error handler '''
    def __init__(self, func):
        self.func = func

    # def input_error(self):
    #     ''' returns FUNCTION, not string !!! '''
    #     def wrapper(self, *args):
    #         try:
    #             result = self.func(*args)
    #         except KeyError:
    #             result = "Not found."
    #         except ValueError:
    #             result = "Entered incorrect data."
    #         except IndexError:
    #             result = "Not enough parameters."
    #         except TypeError:
    #             result = "Sorry, I do not understand."
    #         else:
    #             return result
    #         return f'{RED}{result}{RESET}'
    #     return wrapper

    def __call__(self):
        def wrapper(self, *args):
            try:
                result = self.func(*args)
            except KeyError:
                result = "Not found."
            except ValueError:
                result = "Entered incorrect data."
            except IndexError:
                result = "Not enough parameters."
            except TypeError:
                result = "Sorry, I do not understand."
            else:
                return result
            return f'{RED}{result}{RESET}'
        return wrapper

@ErrorHandler
class Bot():
    '''
    Клас для інтерактивного спілкування з користувачем.
    '''

    def __init__(self) -> None:
        self.address_book = AddressBook()
        self.notes = Notes()
        self.save_file = FILENAME
        self.address_book.load(self.save_file)
        self.notes.load()
        # order MATTERS!!!! Single word command must be in the end !
        self.commands = {
            "hello": self.hello(),
            "hi": self.hello(),
            "help": self.help_(),
            "?": self.help_(),
            "add phone": self.add_phone(),
            "add birthday": self.add_birthday(),
            "add note": self.add_note(),
            "add tags": self.add_tags(),
            "add email": self.add_email(),
            "add address": self.add_adress(),
            "add": self.add_phone(),
            "change address": self.change_adress(),
            "change phone": self.change_phone(),
            "change birthday": self.change_birthday(),
            "change note": self.change_note(),
            "change email": self.change_email(),
            "change": self.change_phone(), 
            "get contact": self.get_phone(),
            "get": self.get_phone(),
            "all": self.all_contacts(),
            "show all": self.all_contacts(),
            "delete phone": self.delete_phone(),
            "delete birthday": self.delete_birthday(),
            "delete note": self.del_note(),
            "delete tags": self.delete_tags(),
            "delete address": self.delete_adress(),
            "delete email": self.delete_email(),
            "delete": self.delete_phone(),
            # "d": self.debug_(),
            "load": self.restore_data_from_file(),
            "save": self.save_data_to_file(),
            "find note": self.find_note(),
            "find": self.random_search(),
            "search": self.random_search(),
            "sort notes": self.sort_notes(),
            "birthdays": self.birthday_in_XX_days(),
            "sort folder": self.sort_folder()
        }

    def parse(self, input_text: str):
        ''' Parse user input '''
        # itereate over keywords dict, not over input words !!!
        for kw, func in self.commands.items():
            if input_text.lower().startswith(kw):
                params = input_text[len(kw):].strip()
                return func, params.split()
        return self.unknown_command(), []

    def hello(self, *args):
        return f'{BLUE}How can I help you?{RESET}'

    # @ErrorHandler.input_error
    def add_phone(self, *args) -> str:
        ''' додавання номеру телефону '''
        contact_name = _name_request(*args)
        if args[1:]:
            new_phone = args[1]
        else:
            new_phone = input(f'{BLUE}Please enter the phone number ({GREEN}10 digits{BLUE}): {RESET}')
        # if contact exist - we add phone to the list, not replace
        if contact_name in self.address_book.data.keys():
            record = self.address_book.data[contact_name]
            record.add_phone(new_phone)
        else:
            record = Record(contact_name)
            record.add_phone(new_phone)
            self.address_book.add_record(record)
        #this should be corrected when there are other fields added
        if args[2:]:
            birthday = args[2]
            record.add_birthday(birthday)
        message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Phone: {RESET}{new_phone}"
        return message

    # @ErrorHandler.input_error
    def add_birthday(self, *args) -> str:
        contact_name = _name_request(*args)
        if args[1:]:
            birthday = args[1]
        else:
            birthday = input(f'{BLUE}Please enter birthday ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
        if contact_name in self.address_book.data.keys():
            record = self.address_book.data[contact_name]
            record.add_birthday(birthday)
        else:
            # entered date instead of contact name
            if datetime.strptime(contact_name, '%Y-%m-%d'):
                raise ValueError
            record = Record(contact_name)
            record.add_birthday(birthday)
            self.address_book.add_record(record)
        return f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Birthday: {RESET}{birthday}"

    # @ErrorHandler.input_error
    def change_phone(self, *args):
        contact_name = _name_request(*args)
        record = self.address_book.data[contact_name]
        if args[2:]:
            old_phone = args[1]
            new_phone = args[2]
        else:
            if args[1:]:
                old_phone = args[1]
            else:
                old_phone = input(f'{BLUE}Please enter old number: {RESET}')
            if not old_phone in ' '.join([phone.value for phone in record.phones]):
                raise KeyError
            new_phone = input(f'{BLUE}Please enter new number ({GREEN}10 digits{BLUE}): {RESET}')
        record.edit_phone(old_phone, new_phone)
        return f"\n{GREEN}Changed:\n  {BLUE}Phone: {RESET}{old_phone} --> {new_phone}"

    # @ErrorHandler.input_error
    def change_birthday(self, *args):
        contact_name = _name_request(*args)
        record = self.address_book.data[contact_name]
        if args[1:]:
            new_birthday = args[1]
        else:
            new_birthday = input(f'{BLUE}Please enter new birthday date ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
        record.add_birthday(new_birthday)
        return f"\n{GREEN}Changed to:{RESET} {new_birthday}"

    # @ErrorHandler.input_error
    def get_phone(self, *args):
        contact_name = _name_request(*args)
        return self.address_book.find(contact_name)

    def all_contacts(self, n=3, *args):
        return self.address_book.iterator(n)

    # @ErrorHandler.input_error
    def help_(self, *args):
        # with open('README.txt', 'r') as fh:
        #     help_bot = fh.read()
        # return help_bot
        return README_TEXT

    def unknown_command(self, *args):
        return f"{RED}I do not understand, please use correct command.{RESET}"

    # @ErrorHandler.input_error
    def delete_phone(self, *args):
        contact_name = _name_request(*args)
        # name not in book
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        # check if phone provided
        if args[1:]:
            # phone provided, so removing phone only
            phones = args[1:]
            record = self.address_book.data[contact_name]
            for phone in phones:
                record.remove_phone(phone)
        else:
            # no phone, remove whole record
            res = input(f"{RED}Are you sure you want to delete contact {BLUE}{contact_name}{RED}? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
            if not res.lower() == "y":
                return f"{GREEN}Contact was {RED}not{GREEN} deleted.{RESET}"
            self.address_book.delete(contact_name)
        return f'{GREEN}Deleted.{RESET}'

    # @ErrorHandler.input_error
    def delete_birthday(aself, *args):
        contact_name = _name_request(*args)
        # name not in book
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        record = self.address_book.data[contact_name]
        delattr(record, "birthday")
        return f'{GREEN}Deleted.{RESET}'

    def restore_data_from_file(self, file_name=FILENAME, *args) -> str:
        ''' restore AddressBook object from the file '''
        self.address_book.load(file_name)
        return file_name

    def save_data_to_file(self, file_name=FILENAME, *args):
        self.address_book.save(file_name)
        self.notes.save()
        return f"{GREEN}Saved to {file_name}{RESET}"

    # @ErrorHandler.input_error
    def add_email(self, *args):
        contact_name = _name_request(*args)
        record = Record(contact_name)
        if contact_name not in list(self.address_book.data.keys()):
            self.address_book.add_record(record)
        if args[1:]:
            email_to_add = args[1]
        else:
            email = input(f"{BLUE}Please enter the email: {RESET}")
            if email in [e.value for e in record.emails]:
                return f"{BLUE}{contact_name} already has this email: {RESET}{email} {BLUE}Skipping...{RESET}"
            email_to_add = email
        self.address_book.find(contact_name).add_email(email_to_add)
        return f"{GREEN}Added: {RESET}{email_to_add}"

    # @ErrorHandler.input_error
    def change_email(self, *args):
        contact_name = _name_request(*args)
        record:Record = self.address_book.data[contact_name]
        if args[2:]:
            old_email = args[1]
            new_email = args[2]
        else:
            old_email = input(f"{BLUE}Please enter email you want to change: {RESET}")
            if old_email not in [e.value for e in record.emails]:
                return f"{BLUE}{contact_name} does not have {RESET}{old_email} {BLUE}Skipping...{RESET}"
            new_email = input(f"{BLUE}Please enter new email: {RESET}")
        record.change_email(old_email, new_email)
        return f"\n{GREEN}Email changed:\n  {RESET}{old_email} --> {new_email}"

    # @ErrorHandler.input_error
    def delete_email(self, *args):
        contact_name = _name_request(*args)
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        record:Record = self.address_book.data[contact_name]
        if args[1:]:
            emails_to_delete = args[1:]
        else:
            emails_to_delete = [input(f"{BLUE}Please enter email: {RESET}")]
        for email in emails_to_delete:
            if email not in [e.value for e in record.emails]:
                return f"{BLUE}{contact_name} does not have such email. Skipping...{RESET}"
            else:
                record.delete_email(email)
        return f'{GREEN}Done.{RESET}'

    # @ErrorHandler.input_error
    def add_adress(self, *args):
        contact_name = _name_request(*args)
        record:Record = self.address_book.data[contact_name]
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        if args[1:]:
            adress_to_add = args[1:]
        else:
            entered = input(f"{BLUE}Enter adress: {RESET}")
            adress_to_add = entered.split(' ')
        if len(adress_to_add[0].strip()) < 1:
            raise ValueError
        if hasattr(record, 'adress'):
            ask = input(f"{BLUE}Previous adress '{record.adress}' will be deleted. OK? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: {RESET}")
            if not ask.lower() == "y":
                return f"{GREEN}New address was {RED}not{GREEN} added.{RESET}"
        adress = ' '.join(str(e).capitalize() for e in adress_to_add)
        self.address_book.find(contact_name).add_adress(adress)
        return f"{GREEN}New adress added: {RESET}{adress}"

    # @ErrorHandler.input_error
    def change_adress(self, *args):
        contact_name = _name_request(*args)
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        if args[1:]:
            new_adress = ' '.join(str(e).capitalize() for e in args[1:])
        else:
            new_adress = [input(f"{BLUE}Please enter new adress: {RESET}")]
            new_adress = new_adress[0].split(" ")
            if not new_adress:
                raise IndexError
            new_adress = ' '.join(str(e).capitalize() for e in new_adress)
        record:Record = self.address_book.data[contact_name]
        delattr(record, "adress")
        record.add_adress(new_adress)
        return f'{GREEN}New adress:\n{RESET}{new_adress}'

    # @ErrorHandler.input_error
    def delete_adress(self, *args):
        contact_name = _name_request(*args)
        if contact_name not in list(self.address_book.data.keys()):
            raise KeyError
        record:Record = self.address_book.data[contact_name]
        if not hasattr(record, "adress"):
            return f"{BLUE}{contact_name} does not have any addresses. Skipping...{RESET}"
        delattr(record, "adress")
        return f'{GREEN}Done.{RESET}'

    # @ErrorHandler.input_error
    def random_search(self, *args) -> GeneratorType:
        search = args[0]
        # do not search if less than 3 symbols entered
        # if first parameter too short and several parameters entered - join all parameters
        if len(search) < 3:
            if len(' '.join(args)) > 2:
                search = ''.join(args)
            elif search.isnumeric():
                ...
            else:
                raise IndexError
        # if search string is a name:
        # TODO: normalize small/big letters
        # TODO: search in email and address
        search_result = AddressBook()
        if search.isnumeric():
            #searching for phone
            for record in self.address_book.values():
                for phone in record.phones:
                    if search in str(phone.value):
                        search_result.add_record(record)
                if hasattr(record, "birthday"):
                    # searching by month and date, not year
                    if search in datetime.strftime(record.birthday.value, '%Y-%m-%d'):
                        search_result.add_record(record)
        else:
            #searching for name
            for name, record in self.address_book.data.items():
                # hardcode to bypass current error with "none" record
                if name is None:
                    continue
                if search.lower() in name.lower():
                    search_result.add_record(record)
                #search on all fields
                if hasattr(record, "emails"):
                    # for email in [record.emails:
                    lst = [x.value for x in record.emails]
                    if search.lower() in ''.join(lst).lower():
                        search_result.add_record(record)
                if hasattr(record, "adress"):
                    if search.lower() in record.adress.lower():
                        search_result.add_record(record)
        if not search_result:
            raise KeyError
        return search_result.iterator(2)

    # @ErrorHandler.input_error
    def birthday_in_XX_days(self, *args):
        ''' знайти всі контакти, у яких день народження за XX днів'''
        return self.address_book.bd_in_xx_days(int(args[0]))


    # @ErrorHandler.input_error
    def add_note(self, *arg):
        note = input(f"{BLUE}Please enter new note: {RESET}")
        if not note:
            res = input(f"{RED}Are you sure you want to save blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
            if not res.lower() == "y":
                return f"{GREEN}Note was {RED}not{GREEN} sasved.{RESET}"
        new_note = NoteRecord(note)
        tags = input(f"{BLUE}Please enter note tags: {RESET}")
        new_note.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
        self.notes.add(new_note)
        self.notes.save()
        return f"{GREEN}The note was saved.{RESET}"

    # @ErrorHandler.input_error
    def find_note(self, *arg):
        find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes: ")
        # тут брєд якийсь, повна надія на ввод тільки t/n
        if find_func in "tags":
            use_func = self.notes.find_by_tag
        elif find_func in "notes":
            use_func = self.notes.find_by_note
        else:
            return f"{RED}You must choose: search by tags or notes.{RESET}"
        request = input(f"{BLUE}Searching for: {RESET}")
        res = use_func(request)
        if not res:
            raise KeyError
        return res

    # @ErrorHandler.input_error
    def _find_note_to_func(self, *arg):
        num = 1
        found_notes = self.find_note(self, *arg)
        if isinstance(found_notes, str):
            return found_notes
        elif len(found_notes) > 1:
            for rec in found_notes:
                print(f"{num}. {rec.note}")
                num += 1
            indx = input(f"{BLUE}Please enter the number of the note you want to edit: {RESET}")
        elif len(found_notes) == 1:
            indx = 1
        print(found_notes[int(indx)-1])
        return found_notes, int(indx)

    # @ErrorHandler.input_error
    def change_note(self, *arg):
        found_notes, indx = self._find_note_to_func(self, *arg)
        changed_note = input(f"{BLUE}Please enter the note to change: {RESET}")
        if not changed_note:
            request = input(f"{RED}Do you want save a blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
            if not request.lower() == "y":
                return f"{GREEN}Note was {RED}not{GREEN} changed. {RESET}"
        found_notes[indx-1].edit_note(changed_note)
        return f"{GREEN}The note was changed.{RESET}"

    # @ErrorHandler.input_error
    def add_tags(self, *arg):
        found_notes, indx = self._find_note_to_func(self, *arg)
        new_tags = input(f"{BLUE}Please enter the tags you want to add: {RESET}")
        found_notes[indx-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
        return f"{GREEN}Tags were added.{RESET}"

    # @ErrorHandler.input_error
    def delete_tags(self, *arg):
        found_notes, indx = self._find_note_to_func(self, *arg)
        tags_to_del = input(f"{BLUE}Please enter the tags you want to delete: {RESET}")
        found_notes[indx-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
        return f"{GREEN}Done.{RESET}"

    # @ErrorHandler.input_error
    def del_note(self, *arg):
        found_notes = self.find_note(self, *arg)
        if isinstance(found_notes, str):
            # does int ever happen ?
            return found_notes
        elif len(found_notes) >= 1:
            num = 1
            for rec in found_notes:
                print(f"{num}. {rec.note}")
                num += 1
            indx = int(input(f"{BLUE}Please enter the number of the note you want to delete: {RESET}")) - 1
        print(found_notes[indx])
        check = input(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if not check.lower() == "y":
            return f"{GREEN}Note was {RED}not{GREEN} deleted.{RESET}"
        notes.delete(found_notes[indx])
        return f"{GREEN}Note was deleted.{RESET}"

    def sort_notes(self, *arg) -> list:
        lst = []
        self.notes.sort(key = lambda x: len(x.tags), reverse=True)
        for i in self.notes:
            lst.append(i)
        return lst

    def sort_folder(*args):
        ''' Sort files from a single folder into categorized folders '''
        if not args:
            folder = input(f"{BLUE}Please enter the folder name: {RESET}")
            if not folder:
                raise IndexError
        else:
            folder = args[0]
        return folder_sort(folder)

