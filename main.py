from types import GeneratorType
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from notes import NoteRecord, add_record, find_by_tag, find_by_note, delete_note, sort_notes, save_notes, load_notes
from classes import Record, AddressBook, Email
import folder_sort


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
ALL_COMMANDS = ["exit", "hello", "help", "add", "add entry", "add record", "add number", "add phone", "set", "change entry", "change record", "change number",
                "change phone", "change", "get entry", "get record", "get number", "get phone", "get all", "get", "show number", "show phone", "all", "show all", "show", 
                "list all", "full", "list", "del", "delete", "remove", "read", "load", "save", "find", "search for", "search", "sort folder", "sort"]
command_completer = WordCompleter(ALL_COMMANDS)

def input_error(func):
    ''' 
    returns FUNCTION, not string !!!
    '''
    def inner(*args):
        try:
            result = func(*args)
        except KeyError:
            result = f"{RED}Not found.{RESET}"
        except ValueError:
            result = f"{RED}Entered incorrect data{RESET}"
        except IndexError:
            result = f"{RED}Not enough parameters.{RESET}"
        except TypeError:
            result = f"{RED}Sorry, I do not understand.{RESET}"
        else:
            return result
        return f'{RED}{result}{RESET}'
    return inner

def hello(*args):
    return BLUE + "How can I help you?" + RESET

@input_error
def add_phone(contact_name: str, *args, **kwargs) -> str:
    if len(args) > 0:
        new_phone = args[0]
    else:
        new_phone = input(f'{GREEN}Please enter the phone number (10 digits): {RESET}')
    # if contact exist - we add phone to the list, not replace
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        record.add_phone(new_phone)
    else:
        record = Record(contact_name)
        record.add_phone(new_phone)
        address_book.add_record(record)
    #this should be corrected when there are other fields added
    if len(args) >=2 :
        birthday = args[1]
        record.add_birthday(birthday)
    message = f"\n{GREEN}Record added:\n  {RESET}Name: {record.name.value}\n  phone: {new_phone}"
    return message

@input_error
def add_birthday(contact_name: str, *args, **kwargs) -> str:
    if len(args) > 0:
        birthday = args[0]
    else:
        birthday = input(f'{GREEN}Please enter birthday (YYYY-MM-DD): {RESET}')
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
    message = f"\n{GREEN}Record added:\n  {RESET}Name: {record.name.value}\n  birthday: {birthday}"
    return message

@input_error
def change_phone(*args):
    if len(args) == 1:
        contact_name = args[0]
    else: 
        contact_name = input(f'{GREEN}Please enter contact name: {RESET}')
    record = address_book.data[contact_name]
    if len(args) == 3:
        old_phone, new_phone = args[1:2]
    else:
        old_phone = input(f'{GREEN}Please enter old number: {RESET}')
        if not old_phone in record.phones:
            raise KeyError
        new_phone = input(f'{GREEN}Please enter new number (10 digits): {RESET}')
    record.edit_phone(old_phone, new_phone)
    return f"\n{GREEN}Changed:\n  {RESET}Name: {record.name.value}\n  Phone: {old_phone} to {new_phone}"

@input_error
def change_birthday(*args):
    if len(args) > 0:
        contact_name = args[0]
    else:
        contact_name = input(f'{GREEN}Please enter contact name: {RESET}')
    record = address_book.data[contact_name]
    if len(args) == 3:
        old_birthday, new_birthday = args[1:]
    else:
        new_birthday = input(f'{GREEN}Please enter new birthday date (YYYY-MM-DD): {RESET}')
    record.add_birthday(new_birthday)
    return f"\n{GREEN}Changed to:{RESET} {new_birthday}"

@input_error
def get_phone(*args):
    return address_book.find(args[0])

def all_contacts(N=3, *args):
    return address_book.iterator(N)

def help_(*args):
    return BLUE + """
    This is an embrione of a phone book CLI app written in python just for practice.
    You may add entries or change phone numbers via CLI.
    That's all it can do.
    Maybe in the future it will be extended, but there are doubts about it.
    Use it as is, or just quit.
    """ + RESET

def unknown_command(*args):
    return f"{RED}I do not understand, please use correct command.{RESET}"

@input_error
def delete_phone(*args):
    contact_name = args[0]
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
        address_book.delete(contact_name)
    return GREEN + "removed" + RESET

@input_error
def delete_birthday(*args):
    contact_name = args[0]
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record = address_book.data[contact_name]
    delattr(record, "birthday")
    return f'{GREEN} Removed {RESET}'

def restore_data_from_file(*args, file_name=FILENAME) -> str:
    ''' restore AddressBook object from the file '''

    # TODO: format selection
    # check if filename provided as non-default argument, else -> request, if empty -> set default
    # if file_name == FILENAME:
    #     entered_file_name = input(f"From what file info should be fetched (default is '{FILENAME}')? ").lower()
    #     if entered_file_name == '':
    #         file_name = FILENAME
    # try:
    #     with open(file_name, 'rb') as fh: 
    #         address_book.data = pickle.load(fh)
    # except FileNotFoundError:
    #     print(BLUE + "File not found, using new file." + RESET)
    address_book.load(file_name)
    return file_name

def save_data_to_file(file_name=FILENAME, *args):
    address_book.save(file_name)
    return f"{GREEN}Saved to {file_name}{RESET}"


@input_error
def add_email(*args):
    name = args[0]
    email_to_add = args[1]
    address_book.find(name).add_email(email_to_add)
    return f"New email added to {name} - {email_to_add}"


@input_error
def change_email(*args):
    contact_name = args[0]
    record:Record = address_book.data[contact_name]
    if len(args) <= 1:
        old_email = input(f"{GREEN}Enter email you want to change: {RESET}")
        if old_email not in [e.value for e in record.emails]:
            return f"{contact_name} don`t have this email - {old_email}. Try again!"
        new_email = input(f"{GREEN}Enter new email: {RESET}")
    else:
        old_email = args[1]
        new_email = args[2]
    record.change_email(old_email, new_email)
    return f"\n{GREEN}{record.name.value}'s email changed:\n  {RESET}{old_email} to {new_email}"


@input_error
def delete_email(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise ValueError
    record:Record = address_book.data[contact_name]
    if args[1:]:
        emails_to_delete = args[1:]
    else:
        emails_to_delete = [input(f"{GREEN}Enter email: {RESET}")]
    for email in emails_to_delete:
        if email not in [e.value for e in record.emails]:
            return f"{contact_name} don`t have this email!"
        else:
            record.delete_email(email)
    return GREEN + f"{contact_name}'s emails deleted" + RESET


@input_error
def add_adress(*args):
    contact_name = args[0]
    record:Record = address_book.data[contact_name]
    if contact_name not in list(address_book.data.keys()):
        raise ValueError
    if len(args) <= 1:
        adress_to_add = [input(f"{GREEN}Enter adress: {RESET}")]
    else:
        adress_to_add = args[1:]
    if len(adress_to_add[0].strip()) < 1:
        raise ValueError
    if record.adress:
        ask = input(f"{GREEN}Previous {contact_name} adress '{record.adress}' will be deleted. Print 'y' to accept: {RESET}")
        if not "y" in ask.lower():
            raise ValueError
    adress = ' '.join(str(e).capitalize() for e in adress_to_add)
    address_book.find(contact_name).add_adress(adress)
    return f"New adress added to {contact_name} - {adress}"


@input_error
def change_adress(*args):
    contact_name = args[0]
    if contact_name not in list(address_book.data.keys()):
        raise ValueError
    if len(args) <= 1:
        new_adress = [input(f"{GREEN}Enter adress: {RESET}")]
        if len(new_adress[0]) < 1:
            raise IndexError
        else:
            new_adress = ' '.join(str(e).capitalize() for e in new_adress[0])
    else:
        new_adress = ' '.join(str(e).capitalize() for e in args[1:])
    record:Record = address_book.data[contact_name]
    record.delete_adress()
    record.add_adress(new_adress)
    return GREEN + f"{contact_name} has new adress:\n{new_adress}" + RESET


@input_error
def delete_adress(contact_name):
    if contact_name not in list(address_book.data.keys()):
        raise ValueError
    record:Record = address_book.data[contact_name]
    record.delete_adress()
    return GREEN + f"{contact_name}`s adress was succesfully deleted!" + RESET


# @input_error
def random_search(*args):
    search = args[0]
    # do not search if less than 3 symbols entered
    if len(search) < 3:
        raise ValueError
    # if search strin is a name:
    # TODO: normalize small/big letters
    search_result = AddressBook()
    if search.isnumeric():
        #searching for phone
        for record in address_book.values():
            for phone in record.phones:
                if search in str(phone.value):
                    search_result.add_record(record)
    else:
        #searching for name
        for name, record in address_book.data.items():
            if search in name:
                search_result.add_record(record)
    return search_result.iterator(2)

@input_error
def birthday_in_XX_days(*args):
    ''' знайти всі контакти, у яких день народження за XX днів'''
    return address_book.bd_in_XX_days(int(args[0]))

def add_note():
    note = input("Print note: ")
    note_rec = NoteRecord(note)
    tags = input("Print tags: ")
    note_rec.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    add_record(note_rec)
    save_notes()
    return f"{GREEN}The note was saved!{RESET}"

@input_error
def find_note():
    find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes.")
    if find_func in "tags":
        use_func = find_by_tag 
    elif find_func in "notes":
        use_func = find_by_note
    else:
        return f"{RED}You must select to search by tags or notes!{RESET}"
    request = input("Print what you search: ")
    res = use_func(request)
    return res if res else f"{RED}No notes found for this request!{RESET}"

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
        indx = input("Write the number of the note you want to edit: ")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    return found_notes, indx

@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = input("Write changed note: ") 
    found_notes[int(indx)-1].edit_note(changed_note)
    return f"{GREEN}Note was changed!{RESET}"

@input_error
def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = input("Write tags you want to add: ")
    found_notes[int(indx)-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
    return f"{GREEN}Tags were added!{RESET}"

def delete_tags():
    found_notes, indx = find_note_to_func()
    tags_to_del = input("Write tags you want to delete: ")
    found_notes[int(indx)-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
    return f"{RED}Tags were deleted!{RESET}"

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
        indx = input("Write the number of the note you want to delete: ")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    check = input("Are you sure you want to delete this entry?(y or n): ")
    if check in "yes":
        delete_note(found_notes[int(indx)-1])
        return f"{RED}Note was deleted!{RESET}"
    else:
        return f"{RED}Note wasn't delete!{RESET}"
        
def sort_folder(*args):
    ''' Sort files from a single folder into categorized folders '''
    if not args:
        folder = input(f"{BLUE}Enter the folder name: {RESET}")
        if not folder:
            raise IndexError
    else:
        folder = args[0]
    return folder_sort.main(folder)


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
                "change email": change_email,
                "delete email": delete_email,
                "add adress": add_adress,
                "change adress": change_adress,
                "delete adress": delete_adress,
                "add": add_phone,
                "change phone": change_phone,
                "change birthday": change_birthday,
                "change note": change_note,
                "change": change_phone, 
                "get contact": get_phone,
                "get": get_phone,
                "all": all_contacts,
                "show all": all_contacts,
                "delete phone": delete_phone,
                "delete birthday": delete_birthday,
                "delete note": del_note,
                "delete tags": delete_tags,

                "delete": delete_phone,
                # "d": debug_,
                "load": restore_data_from_file,
                "save": save_data_to_file,
                "find note": find_note,
                "find": random_search,
                "sort notes": sort_notes,
                "birthdays": birthday_in_XX_days,
                "sort folder": sort_folder
              }

def parse(input_text: str):
    # itereate over keywords dict, not over input words !!!
    for kw, func in OPERATIONS.items():
        if input_text.startswith(kw):
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
        input_ = input_.lower()
        # check if user want to stop, strip() - just in case :)
        if input_.strip() in STOP_WORDS:
            # TODO: format dependent
            save_data_to_file(file_name)
            save_notes()
            print(f"{GREEN}See you, bye!{RESET}")
            break
        # check for empty input, do nothing
        if input_.strip() == '':
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
                _ = input(f"{BLUE}....Press Enter to continue....{RESET}")
        elif isinstance(command_to_run, list):
            for rec in command_to_run:
                print(rec)
        else:
            print(f'{RESET}{command_to_run}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
