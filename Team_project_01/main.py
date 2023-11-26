from types import GeneratorType
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from Team_project_01.notes import *
from Team_project_01.classes import *
import Team_project_01.folder_sort
from Team_project_01.readme import TEXT

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

FILENAME = "book.dat"
STOP_WORDS = [
                'good bye', 
                'goodbye', 
                'bye', 
                'close', 
                'exit', 
                'quit', 
                'stop', 
                'enough',
                'finish',
                'pa',
                'q'
            ]


class Message:
    # абстрактний клас
    def message(self):
        raise NotImplementedError()
    

class NewContactMessage(Message):
    #виводить повідмлення про створення нового контакту
    def __init__(self, name, param=""):
        self.name = name
        self.param = param

    def message(self):
        message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{self.name}\n  {BLUE}Phone: {RESET}{self.param}"
        return message


class PleaseEnterInput(Message):
    # виводить повідомлення з проханням ввести значення
    def __init__(self, param_to_enter:str, add_text:str = ""):
        self.param_to_enter = param_to_enter
        self.add_text = add_text

    def message(self):
        message = input(f'{BLUE}Please enter {self.param_to_enter} {self.add_text}- PleaseEnterInput: {RESET}')
        return message


class DoneMessage(Message):
    # виводить повідомлення про успішне виконання (видалення, зміну, додавання, тощо)
    def __init__(self, done_param_name, activity, done_param=""):
        self.done_param_name = done_param_name
        self.activity = activity
        self.done_param = done_param

    def message(self):
        message = f"{GREEN}{self.done_param_name} was {self.activity}: {RESET}{self.done_param}"
        return message


class NotDoneMessage(Message):
    # виводить повідомлення про НЕуспішне виконання (видалення, зміну, додавання, тощо)
    def __init__(self, not_done_param_name, activity):
        self.not_done_param_name = not_done_param_name
        self.activity = activity

    def message(self):
        message = f"{GREEN}{self.not_done_param_name} was {RED}not{GREEN} {self.activity}.{RESET}"
        return message


class ChangedMessage(Message):
    # виводить повідомлення про успішну зміну параметра
    def __init__(self, changed_param_name, old_param, new_param):
        self.changed_param_name = changed_param_name
        self.old_param = old_param
        self.new_param = new_param
    
    def message(self):
        message = f"\n{GREEN}Changed:\n  {BLUE}{self.changed_param_name}: {RESET}{self.old_param} --> {self.new_param}"
        return message
    

class ParamErrorMessage(Message):
    # виводить повідомлення про те що параметр вже існує або ж він відсутній
    def __init__(self, contact_name, activity, param_name, param = ""):
        self.contact_name = contact_name
        self.activity = activity
        self.param_name = param_name
        self.param = param
    
    def message(self):
        if self.param == "":
            message = f"{BLUE}{self.contact_name} {self.activity} {self.param_name}: {RESET}{self.param} {BLUE}Skipping...{RESET}"
        else:
            message = f"{BLUE}{self.contact_name} {self.activity} {self.param_name}. {BLUE}Skipping...{RESET}"
        return message

def input_error(func):
    ''' 
    returns FUNCTION, not string !!!
    '''
    def inner(*args):
        try:
            result = func(*args)
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
    return inner


def hello(*args):
    return f'{BLUE}How can I help you?{RESET}'


def _name_request(*args) -> str:
    return args[0].strip() if args else PleaseEnterInput("the contact name").message().strip()


#@input_error
def add_phone(*args, **kwargs) -> str:
    contact_name = _name_request(*args)
    if args[1:]:
        new_phone = args[1]
    else:
        new_phone = PleaseEnterInput("the phone number", f"({GREEN}10 digits{BLUE})").message()
    # if contact exist - we add phone to the list, not replace
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        record.add_phone(new_phone)
    else:
        record = Record(contact_name)
        record.add_phone(new_phone)
        address_book.add_record(record)
    #this should be corrected when there are other fields added
    if args[2:]:
        birthday = args[2]
        record.add_birthday(birthday)
    message = NewContactMessage(record.name.value, new_phone).message()
    return message


@input_error
def add_birthday(*args, **kwargs) -> str:
    contact_name = _name_request(*args)
    if args[1:]:
        birthday = args[1]
    else:
        birthday = PleaseEnterInput("birthday", f"({GREEN}YYYY-MM-DD{BLUE})").message()
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        record.add_birthday(birthday)
    else:
        # entered date instead of contact name
        if datetime.strptime(contact_name, '%Y-%m-%d'):
            raise ValueError
        record = Record(contact_name)
        record.add_birthday(birthday)
        address_book.add_record(record)
    message = DoneMessage("Birthday", "added", birthday).message()
    return message


@input_error
def change_phone(*args):
    contact_name = _name_request(*args)
    record = address_book.data[contact_name]
    if args[2:]:
        old_phone = args[1]
        new_phone = args[2]
    else:
        if args[1:]:
            old_phone = args[1]
        else:
            old_phone = PleaseEnterInput("old number").message()
        if not old_phone in ' '.join([phone.value for phone in record.phones]):
            raise KeyError
        new_phone = PleaseEnterInput("new phone number", f"({GREEN}10 digits{BLUE})").message()
    record.edit_phone(old_phone, new_phone)
    return ChangedMessage("Phone", old_phone, new_phone).message()


@input_error
def change_birthday(*args):
    contact_name = _name_request(*args)
    record = address_book.data[contact_name]
    if args[1:]:
        new_birthday = args[1]
    else:
        new_birthday = PleaseEnterInput("new birthday date", f"({GREEN}YYYY-MM-DD{BLUE})").message()
    record.add_birthday(new_birthday)
    return ChangedMessage("Birthday", "", new_birthday).message()

@input_error
def get_phone(*args):
    contact_name = _name_request(*args)
    return address_book.find(contact_name)


def all_contacts(N=3, *args):
    return address_book.iterator(N)


@input_error
def help_(*args):
    return TEXT


def unknown_command(*args):
    return f"{RED}I do not understand, please use correct command.{RESET}"


@input_error
def delete_phone(*args):
    contact_name = _name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    # check if phone provided
    if args[1:]:
        # phone provided, so removing phone only
        phones = args[1:]
        record = address_book.data[contact_name]
        for phone in phones:
            record.remove_phone(phone)
    else:
        # no phone, remove whole record
        res = input(f"{RED}Are you sure you want to delete contact {contact_name}? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if not res.lower() == "y":
            return NotDoneMessage("Contact", "deleted").message()
        address_book.delete(contact_name)
    return DoneMessage("Phone", "deleted", phone).message()


@input_error
def delete_birthday(*args):
    contact_name = _name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record = address_book.data[contact_name]
    delattr(record, "birthday")
    return DoneMessage("Birthday", "deleted").message().replace(":","")

def restore_data_from_file(*args, file_name=FILENAME) -> str:
    ''' restore AddressBook object from the file '''
    address_book.load(file_name)
    return file_name

def save_data_to_file(file_name=FILENAME, *args):
    address_book.save(file_name)
    return DoneMessage("Data", "saved to", file_name).message()


@input_error
def add_email(*args):
    contact_name = _name_request(*args)
    record = Record(contact_name)
    if contact_name not in list(address_book.data.keys()):
        address_book.add_record(record)
    if args[1:]:
        email_to_add = args[1]
    else:
        email = PleaseEnterInput("the email").message()
        if email in [e.value for e in record.emails]:
            return ParamErrorMessage(contact_name, "already has", "email", email).message()
        email_to_add = email
    address_book.find(contact_name).add_email(email_to_add)
    return DoneMessage("Email", "added", email_to_add).message()


@input_error
def change_email(*args):
    contact_name = _name_request(*args)
    record:Record = address_book.data[contact_name]
    if args[2:]:
        old_email = args[1]
        new_email = args[2]
    else:
        old_email = PleaseEnterInput("email you want to change").message()
        if old_email not in [e.value for e in record.emails]:
            return ParamErrorMessage(contact_name, "does not have", "email", old_email).message()
        new_email = PleaseEnterInput("new email").message()
    record.change_email(old_email, new_email)
    return ChangedMessage("Email", old_email, new_email).message()

@input_error
def delete_email(*args):
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if args[1:]:
        emails_to_delete = args[1:]
    else:
        emails_to_delete = [PleaseEnterInput("email").message()]
    for email in emails_to_delete:
        if email not in [e.value for e in record.emails]:
            return ParamErrorMessage(contact_name, "does not have", "email", email).message()
        else:
            record.delete_email(email)
    return DoneMessage("Email", "deleted", email).message()


@input_error
def add_adress(*args):
    contact_name = _name_request(*args)
    record:Record = address_book.data[contact_name]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        adress_to_add = args[1:]
    else:
        entered = PleaseEnterInput("adress").message()
        adress_to_add = entered.split(' ')
    if len(adress_to_add[0].strip()) < 1:
        raise ValueError
    if hasattr(record, 'adress'):
        ask = input(f"{BLUE}Previous adress '{record.adress}' will be deleted. OK? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: {RESET}")
        if not ask.lower() == "y":
            return NotDoneMessage("New address", "added").message()
    adress = ' '.join(str(e).capitalize() for e in adress_to_add)
    address_book.find(contact_name).add_adress(adress)
    return DoneMessage("Adress", "added", adress).message()


@input_error
def change_adress(*args):
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        new_adress = ' '.join(str(e).capitalize() for e in args[1:])
    else:
        new_adress = [PleaseEnterInput("new adress").message()]
        new_adress = new_adress[0].split(" ")
        if not new_adress:
            raise IndexError
        new_adress = ' '.join(str(e).capitalize() for e in new_adress)
    record:Record = address_book.data[contact_name]
    delattr(record, "adress")
    record.add_adress(new_adress)
    return ChangedMessage("Adress", "", new_adress).message()


@input_error
def delete_adress(*args):
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if not hasattr(record, "adress"):
        return ParamErrorMessage(contact_name, "does not have", "any adresses").message()
    delattr(record, "adress")
    return DoneMessage("Adress", "deleted").message().replace(":","")


@input_error
def random_search(*args) -> GeneratorType:
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
        for record in address_book.values():
            for phone in record.phones:
                if search in str(phone.value):
                    search_result.add_record(record)
            if hasattr(record, "birthday"):
                # searching by month and date, not year
                if search in datetime.strftime(record.birthday.value, '%Y-%m-%d'):
                    search_result.add_record(record)
    else:
        #searching for name
        for name, record in address_book.data.items():
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


@input_error
def birthday_in_XX_days(*args):
    ''' знайти всі контакти, у яких день народження за XX днів'''
    return address_book.bd_in_xx_days(int(args[0]))


@input_error
def add_note():
    note = PleaseEnterInput("new note").message()
    if not note:
        res = input(f"{RED}Are you sure you want to save blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if not res.lower() == "y":
            return NotDoneMessage("Note", "saved").message()
    note_rec = NoteRecord(note)
    tags = PleaseEnterInput("note tags").message()
    note_rec.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    add_record(note_rec)
    save_notes()
    return DoneMessage("Note", "saved", note).message()


@input_error
def find_note():
    find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes: ") 
    if find_func in "tags":
        use_func = find_by_tag
    elif find_func in "notes":
        use_func = find_by_note
    else:
        return f"{RED}You must choose: search by tags or notes.{RESET}"
    request = input(f"{BLUE}Searching for: {RESET}")
    res = use_func(request)
    if not res:
        raise KeyError
    return res


@input_error
def find_note_to_func():
    num = 1
    found_notes = find_note()
    if isinstance(found_notes, str):
        return found_notes
    elif len(found_notes) > 1:
        for rec in found_notes:
            print(f"{num}. {rec.note}")
            num += 1
        indx = PleaseEnterInput("the number of the note you want to edit").message()
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    return found_notes, indx


@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = PleaseEnterInput("the note to change").message()
    if not changed_note:
        request = input(f"{RED}Do you want save a blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        if not request.lower() == "y":
            return NotDoneMessage("Note", "changed").message()
    found_notes[int(indx)-1].edit_note(changed_note)
    return ChangedMessage("Note", "", changed_note).message()


@input_error
def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = PleaseEnterInput("the tags you want to add").message()
    new_tags = new_tags.split(", ") if "," in new_tags else new_tags.split(" ")
    found_notes[int(indx)-1].add_tags(new_tags)
    return DoneMessage("Tags", "added", new_tags).message()


@input_error
def delete_tags():
    found_notes, indx = find_note_to_func()
    tags_to_del = PleaseEnterInput("the tags you want to delete").message()
    found_notes[int(indx)-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
    return DoneMessage("Tags", "deleted").message().replace(":", "")


@input_error
def del_note():
    num = 1
    found_notes = find_note()
    if isinstance(found_notes, str):
        return found_notes
    elif len(found_notes) > 1:
        for rec in found_notes:
            print(f"{num}. {rec.note}")
            num += 1
        indx = PleaseEnterInput("the number of the note you want to delete").message()
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    check = input(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
    if not check.lower() == "y":
        return NotDoneMessage("Note", "deleted").message()
    delete_note(found_notes[int(indx)-1])
    return DoneMessage("Note", "deleted").message().replace(":", "")

@input_error
def sort_folder(*args):
    ''' Sort files from a single folder into categorized folders '''
    if not args:
        folder = PleaseEnterInput("the folder name").message()
        if not folder:
            raise IndexError
    else:
        folder = args[0]
    return Team_project_01.folder_sort.main(folder)


address_book = AddressBook()

# order MATTERS!!!! Single word command must be in the end !
OPERATIONS = {
                "hello": hello,
                "help": help_,
                "?": help_,
                "add phone": add_phone,
                "add birthday": add_birthday,
                "add note": add_note,
                "add tags": add_tags,
                "add email": add_email,
                "add address": add_adress,
                "add": add_phone,
                "change address": change_adress,
                "change phone": change_phone,
                "change birthday": change_birthday,
                "change note": change_note,
                "change email": change_email,
                "change": change_phone, 
                "get contact": get_phone,
                "get": get_phone,
                "all": all_contacts,
                "show all": all_contacts,
                "delete phone": delete_phone,
                "delete birthday": delete_birthday,
                "delete note": del_note,
                "delete tags": delete_tags,
                "delete address": delete_adress,
                "delete email": delete_email,
                "delete": delete_phone,
                # "d": debug_,
                "load": restore_data_from_file,
                "save": save_data_to_file,
                "find note": find_note,
                "find": random_search,
                "search": random_search,
                "sort notes": sort_notes,
                "birthdays": birthday_in_XX_days,
                "sort folder": sort_folder
              }

ALL_COMMANDS = OPERATIONS.keys()
command_completer = WordCompleter(ALL_COMMANDS, sentence=True, ignore_case=True)

def parse(input_text: str):
    # itereate over keywords dict, not over input words !!!
    for kw, func in OPERATIONS.items():
        if input_text.lower().startswith(kw):
            params = input_text[len(kw):].strip()
            return func, params.split()
    return unknown_command, []


def main():
    ''' main cycle'''
    # file_name = restore_data_from_file()
    # entered_file_name = input(f"From what file info should be fetched (default is '{FILENAME}')? ").lower()
    #file_name = FILENAME if entered_file_name == '' else entered_file_name
    file_name = FILENAME
    address_book.load(file_name)
    load_notes()
    while True:
        input_ = prompt(">>> ", completer=command_completer)
        input_ = input_.strip()
        # check if user want to stop, strip() - just in case :)
        if input_.lower() in STOP_WORDS:
            # TODO: format dependent
            save_data_to_file(file_name)
            save_notes()
            print(f"{GREEN}See you, bye!{RESET}")
            break
        # check for empty input, do nothing
        if not input_:
            continue
        # simple split() does not allow to use spaces in OPERATIONS dict
        command, parameters = parse(input_)
        # all -> generator
        # other commands -> str
        command_to_run = command(*parameters)
        if isinstance(command_to_run, GeneratorType):
            for _selection in command_to_run:
                for _entry in _selection:
                    print(_entry)
                    print('----------')
                _ = input(f"{RESET}....Press {BLUE}Enter{RESET} to continue....\n")
        elif isinstance(command_to_run, list):
            for rec in command_to_run:
                print(rec)
        else:
            print(f'{RESET}{command_to_run}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
