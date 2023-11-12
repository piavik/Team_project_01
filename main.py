from types import GeneratorType
from datetime import datetime
from classes import Record, AddressBook
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
            result = "Entered incorrect data"
        except IndexError:
            result = "Not enough parameters."
        except TypeError:
            result = "Sorry, I do not understand."
        else:
            return f'{GREEN}{result}{RESET}'
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
def sort_folder(*args):
    ''' Sort files from a single folder into categorized folders '''
    if not args:
        folder = input(f"{GREEN}Enter the folder name: {RESET}")
    else:
        folder = args[0]
    return folder_sort.main(folder)


address_book = AddressBook()

# order MATTERS!!!! Single word command must be in the end !
OPERATIONS = {
                "hello": hello,
                "hi": hello,
                "help": help_,
                "?": hello,
                "add entry": add_phone,
                "add record": add_phone,
                "add number": add_phone,
                "add phone": add_phone,
                "add birthday": add_birthday,
                "add": add_phone,
                "set": add_phone,
                "change entry": change_phone,
                "change record": change_phone,
                "change number": change_phone,
                "change phone": change_phone,
                "change birthday": change_birthday,
                "change": change_phone, 
                "get entry": get_phone,
                "get record": get_phone,
                "get number": get_phone,
                "get phone": get_phone,
                "get all": all_contacts,
                "get": get_phone,
                "show number": get_phone,
                "show phone": get_phone,
                "all": all_contacts,
                "show all": all_contacts,
                "show": get_phone,
                "list all": all_contacts,
                "full": all_contacts,
                "list": all_contacts,
                "del phone": delete_phone,
                "delete phone": delete_phone,
                "delete birthday": delete_birthday,
                "del birthday": delete_birthday,
                "delete": delete_phone,
                "del": delete_phone,
                "remove": delete_phone,
                # "d": debug_,
                "read": restore_data_from_file,
                "load": restore_data_from_file,
                "save": save_data_to_file,
                "find": random_search,
                "search for": random_search,
                "search": random_search,
                "sort folder": sort_folder,
                "sort": sort_folder,
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
    while True:
        input_ = input(">>>").lower()
        # check if user want to stop, strip() - just in case :)
        if input_.strip() in STOP_WORDS:
            # TODO: format dependent
            save_data_to_file(file_name)
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
        else:
            print(f'{RESET}{command_to_run}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
