from Team_project_01.constants import RED, BLUE, GREEN, RESET
from Team_project_01.functions_common import input_error, name_request, yes_no


@input_error
def add_phone(*args, **kwargs) -> str:
    ''' додавання телефону контакту '''
    contact_name = name_request(*args)
    if args[1:]:
        new_phone = args[1]
    else:
        new_phone = input(f'{BLUE}Please enter the phone number ({GREEN}10 digits{BLUE}): {RESET}')
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
    message = f"\n{GREEN}Record added:\n  {BLUE}Name: {RESET}{record.name.value}\n  {BLUE}Phone: {RESET}{new_phone}"
    return message

@input_error
def change_phone(*args):
    ''' зміна телефону контакту '''
    contact_name = name_request(*args)
    record = address_book.data[contact_name]
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

@input_error
def delete_phone(*args):
    ''' видалення телефону контакту, або всього контакту '''
    contact_name = name_request(*args)
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
        if not yes_no(f"Are you sure you want to delete contact {contact_name}?"):
            return f"{GREEN}Contact was {RED}not{GREEN} deleted.{RESET}"
        address_book.delete(contact_name)
    return f'{GREEN}Deleted.{RESET}'
