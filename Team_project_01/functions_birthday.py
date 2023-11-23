from datetime import datetime
from Team_project_01.constants import RED, BLUE, GREEN, RESET
from Team_project_01.functions_common import input_error, name_request
from Team_project_01.functions_common import input_error, name_request

@input_error
def add_birthday(*args, **kwargs) -> str:
    ''' додавання дня народження '''
    contact_name = name_request(*args)
    if args[1:]:
        birthday = args[1]
    else:
        birthday = input(f'{BLUE}Please enter birthday ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
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
    message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Birthday: {RESET}{birthday}"
    return message

@input_error
def change_birthday(*args):
    ''' зміна дня народження '''
    contact_name = name_request(*args)
    record = address_book.data[contact_name]
    if args[1:]:
        new_birthday = args[1]
    else:
        new_birthday = input(f'{BLUE}Please enter {GREEN}new{BLUE} birthday date ({GREEN}YYYY-MM-DD{BLUE}): {RESET}')
    record.add_birthday(new_birthday)
    return f"\n{GREEN}Changed to:{RESET} {new_birthday}"

@input_error
def delete_birthday(*args):
    ''' видалення дня народження '''
    contact_name = name_request(*args)
    # name not in book
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record = address_book.data[contact_name]
    delattr(record, "birthday")
    return f'{GREEN}Deleted.{RESET}'
