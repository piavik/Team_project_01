from Team_project_01.constants import RED, BLUE, GREEN, RESET
from Team_project_01.functions_common import input_error, name_request, yes_no


@input_error
def add_adress(*args):
    ''' додавання адреси '''
    contact_name = name_request(*args)
    record:Record = address_book.data[contact_name]
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        adress_to_add = args[1:]
    else:
        entered = input(f"{BLUE}Enter adress: {RESET}")
        adress_to_add = entered.split(' ')
    if len(adress_to_add[0].strip()) < 1:
        raise ValueError
    if hasattr(record, 'adress'):
        if not yes_no(f'Previous adress "{record.adress}" will be deleted. OK?'):
            return f"{GREEN}Contact was {RED}not{GREEN} deleted.{RESET}"
    adress = ' '.join(str(e).capitalize() for e in adress_to_add)
    address_book.find(contact_name).add_adress(adress)
    return f"{GREEN}New adress added: {RESET}{adress}"

@input_error
def change_adress(*args):
    ''' зміна адреси '''
    contact_name = name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    if args[1:]:
        new_adress = ' '.join(str(e).capitalize() for e in args[1:])
    else:
        new_adress = [input(f"{BLUE}Please enter {GREEN}new{BLUE} adress: {RESET}")]
        new_adress = new_adress[0].split(" ")
        if not new_adress:
            raise IndexError
        new_adress = ' '.join(str(e).capitalize() for e in new_adress)
    record:Record = address_book.data[contact_name]
    delattr(record, "adress")
    record.add_adress(new_adress)
    return f'{GREEN}New adress:\n{RESET}{new_adress}'

@input_error
def delete_adress(*args):
    ''' видалення адреси '''
    contact_name = name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
    if not hasattr(record, "adress"):
        return f"{BLUE}{contact_name} does not have any addresses. Skipping...{RESET}"
    delattr(record, "adress")
    return f'{GREEN}Done.{RESET}'
