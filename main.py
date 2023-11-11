from classes import Record, AddressBook
from notes import NoteRecord, add_record, find_by_tag, find_by_note, delete_note, sort_notes, save_notes, load_notes
from types import GeneratorType


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
            result = "Not found. Unknown record."
        except ValueError:
            result = "Entered incorrect data"
        except IndexError:
            result = "Not enough parameters."
        except TypeError:
            result = "Sorry, I do not understand."
        return "{}{}{}".format(RED,result,RESET)
    return inner

def hello(*args):
    return BLUE + "How can I help you?" + RESET

@input_error
def add_(contact_name, new_phone, birthday=None):
    # with "birthday" field it is necessary to remove the feature 
    # to add several phones at a time
    # so phones are added one by one now
    # if exist - we add phone to the list, not replace
    if contact_name in address_book.data.keys():
        record = address_book.data[contact_name]
        if birthday:
            record.add_birthday(birthday)
        record.add_phone(new_phone)
    else:
        record = Record(contact_name)
        if birthday:
            record.add_birthday(birthday)
        record.add_phone(new_phone)
        address_book.add_record(record)
    message = f"\n{GREEN}Record added:\n  {RESET}Name: {record.name.value}\n  phone: {new_phone}"
    return message

@input_error
def change(*args):
    contact_name = args[0]
    old_phone, new_phone = args[1:]
    record = address_book.data[contact_name]
    record.edit_phone(old_phone, new_phone)
    return f"\n{GREEN}Changed:\n  {RESET}{record.name.value}\n  {old_phone} to {new_phone}"

@input_error
def get_phone(*args):
    return address_book.find(args[0])

def all_(N=3, *args):
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
        raise ValueError
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

def add_note():
    note = input("Print note: ")
    note_rec = NoteRecord(note)
    tags = input("Print tags: ")
    note_rec.add_tags(tags.split(", "))
    add_record(note_rec)
    save_notes()
    return f"{GREEN}The note was saved!{RESET}"

def find_note():
    find_func = input("Select search by tags or notes(Print t or n).")
    use_func = find_by_tag if find_func == "t" else find_by_note
    request = input("Print what you search: ")
    return use_func(request)

def find_note_to_func():
    num = 1
    found_notes = find_note()
    if len(found_notes) > 1:
        for rec in found_notes:
            print(f"{num}. {rec.note}")
            num += 1
        indx = input("Write the number of the note you want to edit: ")
    elif len(found_notes) == 1:
        indx = 1
    else:
        return f"{RED}There is no such note.{RESET}"
    print(found_notes[int(indx)-1])
    return found_notes, indx

@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = input("Write changed note: ") 
    found_notes[int(indx)-1].edit_note(changed_note)
    return f"{GREEN}Note was changed!{RESET}"

def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = input("Write tags you want to add: ")
    found_notes[int(indx)-1].add_tags(new_tags.split(", "))
    return f"{GREEN}Tags were added!{RESET}"

def del_note():
    found_notes, indx = find_note_to_func()
    check = input("Are you sure you want to delete this entry?(y or n): ")
    if check == "y":
        delete_note(found_notes[int(indx-1)])
        return f"{RED}Note was deleted!{RESET}"
    else:
        return f"{RED}Note wasn't delete!{RESET}"
        
address_book = AddressBook()

# order MATTERS!!!! Single word command must be in the end !
OPERATIONS = {
                "hello": hello,
                "hi": hello,
                "help": help_,
                "?": hello,
                "add entry": add_,
                "add record": add_,
                "add number": add_,
                "add phone": add_,
                "add note": add_note,
                "add tags": add_tags,
                "add": add_,
                "set": add_,
                "change entry": change,
                "change record": change,
                "change number": change,
                "change phone": change,
                "change note": change_note,
                "change": change, 
                "get entry": get_phone,
                "get record": get_phone,
                "get number": get_phone,
                "get phone": get_phone,
                "get all": all_,
                "get": get_phone,
                "show number": get_phone,
                "show phone": get_phone,
                "all": all_,
                "show all": all_,
                "show": get_phone,
                "list all": all_,
                "full": all_,
                "list": all_,
                "delete note": del_note,
                "del": delete_phone,
                "delete": delete_phone,
                "remove": delete_phone,
                # "d": debug_,
                "read": restore_data_from_file,
                "load": restore_data_from_file,
                "save": save_data_to_file,
                "find note": find_note,
                "find": random_search,
                "sort notes": sort_notes,
                "search for": random_search,
                "search": random_search
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
    entered_file_name = input(f"From what file info should be fetched (default is '{FILENAME}')? ").lower()
    file_name = FILENAME if entered_file_name == '' else entered_file_name
    address_book.load(file_name)
    load_notes()
    while True:
        input_ = input(">>>").lower()
        # check if user want to stop, strip() - just in case :)
        if input_.strip() in STOP_WORDS:
            print(f"{GREEN}See you, bye!{RESET}")
            # TODO: format dependent
            save_data_to_file(file_name)
            save_notes()
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
                _ = input(f"{BLUE}....Press Enter to continue....{RESET}")
        elif isinstance(command_to_run, list):
            for rec in command_to_run:
                print(rec)
        else:
            print(f'{RESET}{command_to_run}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
