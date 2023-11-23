from types import GeneratorType
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from Team_project_01.constants import *
from Team_project_01.functions_common import input_error, name_request
from Team_project_01.classes import *
from Team_project_01.notes import *
import Team_project_01.folder_sort


def hello(*args):
    return f'{BLUE}How can I help you?{RESET}'

@input_error
def get_phone(*args):
    contact_name = _name_request(*args)
    return address_book.find(contact_name)

def all_contacts(N=3, *args):
    return address_book.iterator(N)

@input_error
def help_(*args):
    # with open('README.txt', 'r') as fh:
    #     help_bot = fh.read()
    # return help_bot
    return README

def unknown_command(*args):
    return f"{RED}I do not understand, please use correct command.{RESET}"

def restore_data_from_file(*args, file_name=FILENAME) -> str:
    ''' restore AddressBook object from the file '''
    address_book.load(file_name)
    return file_name

def save_data_to_file(file_name=FILENAME, *args):
    address_book.save(file_name)
    return f"{GREEN}Saved to {file_name}{RESET}"

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

def sort_folder(*args):
    ''' Sort files from a single folder into categorized folders '''
    if not args:
        folder = input(f"{BLUE}Please enter the folder name: {RESET}")
        if not folder:
            raise IndexError
    else:
        folder = args[0]
    return Team_project_01.folder_sort.main(folder)

def parse(input_text: str):
    # itereate over keywords dict, not over input words !!!
    for kw, func in OPERATIONS.items():
        if input_text.lower().startswith(kw):
            params = input_text[len(kw):].strip()
            return func, params.split()
    return unknown_command, []

address_book = AddressBook()

ALL_COMMANDS = OPERATIONS.keys()
command_completer = WordCompleter(ALL_COMMANDS, sentence=True, ignore_case=True)

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
