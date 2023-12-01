from types import GeneratorType
from datetime import datetime
from functools import wraps
from Team_project_01.classes import Record, AddressBook
from Team_project_01.notes import Notes, NoteRecord
from Team_project_01.folder_sort import folder_sort
from Team_project_01.constants import *
from Team_project_01.class_input_output import Console

console = Console()

def input_error(func):
    ''' 
    returns FUNCTION, not string !!!
    '''
    @wraps(func)
    def wrapper(*args):
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
        except FileNotFoundError:
            result = "File not found, using new book."
        else:
            return result
        return f'{RED}{result}{RESET}'
    return wrapper

def hello(*args) -> str:
    return f'{BLUE}How can I help you?{RESET}'

def _name_request(*args) -> str:
    # return args[0].strip() if args else input(f"{BLUE}Please enter the contact name: {RESET}").strip()
    return console.input(*args, prompt='Please enter the contact name')

@input_error
def add_phone(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    # if args[1:]:
    #     new_phone = args[1]
    # else:
    #     # new_phone = input(f'{BLUE}Please enter the phone number ({GREEN}10 digits{BLUE}): {RESET}')
    new_phone = console.input(*args[1:], prompt=f'Please enter the phone number ({GREEN}10 digits{BLUE})')
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
    message = ( 
        f"\n{GREEN}Record added:\n"
        f"  {BLUE}Name: {RESET}{record.name.value}\n"
        f"  {BLUE}Phone: {RESET}{new_phone}"
    )
    return message

@input_error
def add_birthday(address_book, notes,  *args) -> str:
    contact_name = _name_request(*args)
    # if args[1:]:
    #     birthday = args[1]
    # else:
    #     # birthday = input(f'{BLUE}Please enter birthday ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
    birthday = console.input(*args[1:], prompt=f'Please enter birthday ({GREEN}YYYY-MM-DD{BLUE})')
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
    message =(
        f"\n{GREEN}Record added:\n"
        f"  {BLUE}Name: {RESET}{record.name.value}\n"
        f"  {BLUE}Birthday: {RESET}{birthday}"
    )
    return message

@input_error
def change_phone(address_book, notes,  *args) -> str:
    contact_name = _name_request(*args)
    record = address_book.data[contact_name]
    if args[2:]:
        old_phone = args[1]
        new_phone = args[2]
    else:
        # if args[1:]:
        #     old_phone = args[1]
        # else:
        #     # old_phone = input(f'{BLUE}Please enter old number: {RESET}')
        old_phone = console.input(*args[1:], prompt='Please enter old number')
        if not old_phone in ' '.join([phone.value for phone in record.phones]):
            raise KeyError
        # new_phone = input(f'{BLUE}Please enter new number ({GREEN}10 digits{BLUE}): {RESET}')
        new_phone = console.input(prompt=f'Please enter new number ({GREEN}10 digits{BLUE})')
    record.edit_phone(old_phone, new_phone)
    message = (
        f"\n{GREEN}Changed:\n"
        f"  {BLUE}Phone: {RESET}{old_phone} --> {new_phone}"
    )
    return message

@input_error
def change_birthday(address_book, notes,  *args) -> str:
    contact_name = _name_request(*args)
    record = address_book.data[contact_name]
    # if args[1:]:
    #     new_birthday = args[1]
    # else:
    #     # new_birthday = input(f'{BLUE}Please enter new birthday date ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
    new_birthday = console.input(*args[1:], prompt=f'Please enter new birthday date ({GREEN}YYYY-MM-DD{BLUE})')
    record.add_birthday(new_birthday)
    message = f"\n{GREEN}Changed to:{RESET} {new_birthday}"
    return message

@input_error
def get_phone(address_book, notes,  *args) -> str:
    contact_name = _name_request(*args)
    return address_book.find(contact_name)

def all_contacts(address_book, notes, n=3, *args) -> str:
    return address_book.iterator(n)

@input_error
def help_(*args) -> str:
    # with open('README.txt', 'r') as fh:
    #     help_bot = fh.read()
    # return help_bot
    return README_TEXT

def unknown_command(*args) -> str:
    return f"{RED}I do not understand, please use correct command.{RESET}"

@input_error
def delete_contact(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    confirmed = console.confirm(f"Are you sure you want to delete the contact?")
    if not confirmed:
        return f"{GREEN}Contact was {RED}not{GREEN} deleted.{RESET}"
    address_book.delete(contact_name)
    return f'{GREEN}Deleted.{RESET}'

@input_error
def delete_phone(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    # check if phone provided
    phone = console.input(*args[1:], 'Please enter the phone number you want to delete')
    if phone:
        record = address_book.data[contact_name]
        record.remove_phone(phone)
        return f'{GREEN}Deleted.{RESET}'
    else:
        # no phone, remove whole record
        return delete_contact(address_book, notes, contact_name)


@input_error
def delete_birthday(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record = address_book.data[contact_name]
    delattr(record, "birthday")
    return f'{GREEN}Deleted.{RESET}'

@input_error
def restore_data_from_file(address_book, notes, file_name=FILENAME, *args) -> str:
    ''' restore AddressBook object from the file '''
    address_book.load(file_name)
    notes.load()
    return f"{GREEN}Loaded from {file_name}{RESET}"

def save_data_to_file(address_book, notes, file_name=FILENAME, *args) -> str:
    address_book.save(file_name)
    notes.save(file_name)
    return f"{GREEN}Saved to {file_name}{RESET}"

@input_error
def add_email(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    record = Record(contact_name)
    if contact_name not in list(address_book.data.keys()):
        address_book.add_record(record)
    # if args[1:]:
    #     email_to_add = args[1]
    # else:
    #     # email = input(f"{BLUE}Please enter the email: {RESET}")
        
    email = console.input(*args[1:], prompt='Please enter the email')
    if email in [e.value for e in record.emails]:
        return f"{BLUE}{contact_name} already has this email: {RESET}{email} {BLUE}Skipping...{RESET}"
    email_to_add = email
    address_book.find(contact_name).add_email(email_to_add)
    return f"{GREEN}Added: {RESET}{email_to_add}"

@input_error
def change_email(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    record:Record = address_book.data[contact_name]
    if args[2:]:
        old_email = args[1]
        new_email = args[2]
    else:
        # old_email = input(f"{BLUE}Please enter email you want to change: {RESET}")
        old_email = console.input(prompt='Please enter email you want to change')
        if old_email not in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} does not have {RESET}{old_email} {BLUE}Skipping...{RESET}"
        # new_email = input(f"{BLUE}Please enter new email: {RESET}")
        new_email = console.input(prompt='Please enter new email')
    record.change_email(old_email, new_email)
    message = (
        f"\n{GREEN}Email changed:\n"
        f"  {RESET}{old_email} --> {new_email}"
    )
    return message

@input_error
def delete_email(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    emails_to_delete = [console.input(*args[1:], prompt='Please enter email')]
    for email in emails_to_delete:
        if email not in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} does not have such email. Skipping...{RESET}"
        else:
            record.delete_email(email)
    return f'{GREEN}Done.{RESET}'

@input_error
def add_adress(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    record:Record = address_book.data[contact_name]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    # if args[1:]:
    #     adress_to_add = args[1:]
    # else:
    #     # entered = input(f"{BLUE}Enter adress: {RESET}")ad
    entered = console.input(*args[1:], prompt='Enter adress')
    adress_to_add = entered.split(' ')
    if len(adress_to_add[0].strip()) < 1:
        raise ValueError
    if hasattr(record, 'adress'):
        # ask = input(f"{BLUE}Previous adress '{record.adress}' will be deleted. OK? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: {RESET}")
        confirmed = console.confirm(f'Previous adress "{record.adress}" will be deleted. Is it OK?')
        # if not confirmed.lower() == "y":
        if not confirmed:
            return f"{GREEN}New address was {RED}not{GREEN} added.{RESET}"
    adress = ' '.join(str(e).capitalize() for e in adress_to_add)
    address_book.find(contact_name).add_adress(adress)
    return f"{GREEN}New adress added: {RESET}{adress}"

@input_error
def change_adress(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        new_adress = ' '.join(str(e).capitalize() for e in args[1:])
    else:
        new_adress = [console.input(prompt='Please enter new adress')]
        new_adress = new_adress[0].split(" ")
        if not new_adress:
            raise IndexError
        new_adress = ' '.join(str(e).capitalize() for e in new_adress)
    record:Record = address_book.data[contact_name]
    delattr(record, "adress")
    record.add_adress(new_adress)
    return f'{GREEN}New adress:\n{RESET}{new_adress}'

@input_error
def delete_adress(address_book, notes, *args) -> str:
    contact_name = _name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if not hasattr(record, "adress"):
        return f"{BLUE}{contact_name} does not have any addresses. Skipping...{RESET}"
    delattr(record, "adress")
    return f'{GREEN}Done.{RESET}'

@input_error
def random_search(address_book, notes, *args) -> GeneratorType:
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
def birthday_in_XX_days(address_book, notes, *args) -> str:
    ''' знайти всі контакти, у яких день народження за XX днів'''
    # TODO: без аргументів == сьогодні
    return address_book.bd_in_xx_days(int(args[0]))


@input_error
def add_note(address_book, notes, *arg) -> str:
    note = console.input(prompt='Please enter new note')
    if not note:
        # res = input(f"{RED}Are you sure you want to save blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        confirmed = console.confirm('Are you sure you want to save blank note?')
        # if not confirmed.lower() == "y":
        if not confirmed:
            return f"{GREEN}Note was {RED}not{GREEN} saved.{RESET}"
    new_note = NoteRecord(note)
    # tags = input(f"{BLUE}Please enter note tags: {RESET}")
    tags = console.input(prompt="Please enter note's tags")
    new_note.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    notes.add(new_note)
    notes.save()
    return f"{GREEN}The note was saved.{RESET}"

# -> str or list
@input_error
def find_note(address_book, notes, *arg):
    # find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes: ")
    find_func = console.input(prompt=f'Select search by {GREEN}[t]{BLUE}ags or notes')
    user_request = console.input(prompt='Searching for')
    if find_func.lower() == 't':
        res = notes.find_by_tag(user_request)
    else:
        res = notes.find_by_note(user_request)
    if not res:
        raise KeyError
    return res

# -> list, int
@input_error
def _find_note_to_func(notes, *arg):
    num = 1
    found_notes = find_note(notes, notes, *arg)
    if isinstance(found_notes, str):
        return found_notes
    elif len(found_notes) > 1:
        for rec in found_notes:
            console.output(f"{num}. {rec.note}")
            num += 1
        # indx = input(f"{BLUE}Please enter the number of the note you want to edit: {RESET}")
        indx = console.input(prompt='Please enter the number of the note you want to edit')
    elif len(found_notes) == 1:
        indx = 1
    console.output(found_notes[int(indx)-1])
    return found_notes, int(indx)

@input_error
def change_note(address_book, notes, *arg) -> str:
    found_notes, indx = _find_note_to_func(notes, *arg)
    # changed_note = input(f"{BLUE}Please enter the note to change: {RESET}")
    changed_note = console.input(prompt='Please enter the note to change')
    if not changed_note:
        # request = input(f"{RED}Do you want save a blank note? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
        confirmed = console.confirm('Do you want save a blank note?')
        if not confirmed:
            return f"{GREEN}Note was {RED}not{GREEN} changed. {RESET}"
    found_notes[indx-1].edit_note(changed_note)
    return f"{GREEN}The note was changed.{RESET}"

@input_error
def add_tags(address_book, notes, *arg) -> str:
    found_notes, indx = _find_note_to_func(notes, *arg)
    # new_tags = input(f"{BLUE}Please enter the tags you want to add: {RESET}")
    new_tags = console.input(prompt='Please enter the tags you want to add')
    found_notes[indx-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
    return f"{GREEN}Tags were added.{RESET}"

@input_error
def delete_tags(address_book, notes, *arg) -> str:
    found_notes, indx = _find_note_to_func(notes, *arg)
    # tags_to_del = input(f"{BLUE}Please enter the tags you want to delete: {RESET}")
    tags_to_del = console.input(prompt='Please enter the tags you want to delete')
    found_notes[indx-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
    return f"{GREEN}Done.{RESET}"

@input_error
def del_note(address_book, notes, *arg) -> str:
    found_notes = find_note(address_book, notes, *arg)
    if isinstance(found_notes, str):
        # does int ever happen ?
        return found_notes
    elif len(found_notes) >= 1:
        num = 1
        for rec in found_notes:
            console.output(f"{num}. {rec.note}")
            num += 1
        indx = int(console.input(prompt='Please enter the number of the note you want to delete')) - 1
    console.output(found_notes[indx])
    # check = input(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
    confirmed = console.confirm('Are you sure you want to delete this entry?')
    if not confirmed:
        return f"{GREEN}Note was {RED}not{GREEN} deleted.{RESET}"
    notes.delete(found_notes[indx])
    return f"{GREEN}Note was deleted.{RESET}"

def sort_notes(address_book, notes, *arg) -> list:
    lst = []
    notes.sort(key = lambda x: len(x.tags), reverse=True)
    for i in notes:
        lst.append(i)
    return lst

@input_error
def sort_folder(address_book, notes, *args) -> str:
    ''' Sort files from a single folder into categorized folders '''
    # if not args:
    folder = console.input(*args, prompt='Please enter the folder name')
    if not folder:
        raise IndexError
    # else:
    #     folder = args[0]
    return folder_sort(folder)

def parse(commands: dict, input_text: str) -> tuple:
    # itereate over keywords dict, not over input words !!!
    for kw, func in commands.items():
        if input_text.lower().startswith(kw):
            params = input_text[len(kw):].strip()
            return func, params.split()
    return unknown_command, []

def main() -> None:
    ''' main cycle'''
    # file_name = restore_data_from_file()
    # entered_file_name = input(f"From what file info should be fetched 
    # (default is '{FILENAME}')? ").lower()
    #file_name = FILENAME if entered_file_name == '' else entered_file_name
    file_name = FILENAME
    address_book = AddressBook()
    notes = Notes()
    address_book.load(file_name)
    notes.load()
    # order MATTERS!!!! Single word command must be in the end !
    commands = {
        "hello": hello,
        "hi": hello,
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
        "delete": delete_contact,
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
    command_hints = commands.keys()
    while True:
        # input_ = prompt(">>> ", completer=command_completer)
        input_ = console.hinted_input(command_hints)
        input_ = input_.strip()
        # console = Console()
        # check if user want to stop, strip() - just in case :)
        if input_.lower() in STOP_WORDS:
            # TODO: format dependent
            address_book.save(file_name)
            notes.save()
            console.output(f"{GREEN}See you, bye!{RESET}")
            break
        # check for empty input, do nothing
        if not input_:
            continue
        # simple split() does not allow to use spaces in commands dict
        command, parameters = parse(commands, input_)
        # all -> generator
        # other commands -> str
        result = command(address_book, notes, *parameters)
        if isinstance(result, GeneratorType):
            for _selection in result:
                for _entry in _selection:
                    console.output(_entry)
                    console.output('----------')
                try:
                    # brk = input(f"{RESET}....Press {BLUE}Enter{RESET} to continue, or {BLUE}'q'{RESET} to stop....\n")
                    brk = console.input(prompt=f'{RESET}....Press {BLUE}"q"{RESET} to stop or any key to continue....\n')
                    if brk.lower() == 'q':
                        break
                except KeyboardInterrupt:
                    console.output('\n')
                    break
        elif isinstance(result, list):
            for rec in result:
                console.output(rec)
        else:
            console.output(f'{RESET}{result}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
