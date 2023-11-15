from Team_project_01.constants import RED, BLUE, GREEN, RESET
from Team_project_01.functions_common import input_error, name_request


@input_error
def add_email(*args):
    ''' додавання емейла '''
    contact_name = name_request(*args)
    record = Record(contact_name)
    if contact_name not in list(address_book.data.keys()):
        address_book.add_record(record)
    # only 1 argument used, others are ignored !!!
    if args[1:]:
        email_to_add = args[1]
    else:
        email = input(f"{BLUE}Please enter the email: {RESET}")
        if email in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} already has this email: {RESET}{email} {BLUE}Skipping...{RESET}"
        email_to_add = email
    address_book.find(contact_name).add_email(email_to_add)
    return f"{GREEN}Added: {RESET}{email_to_add}"

@input_error
def change_email(*args):
    ''' зміна емейла '''
    contact_name = name_request(*args)
    record:Record = address_book.data[contact_name]
    if args[2:]:
        old_email = args[1]
        new_email = args[2]
    else:
        old_email = input(f"{BLUE}Please enter email you want to change: {RESET}")
        if old_email not in [e.value for e in record.emails]:
            return f"{BLUE}{contact_name} does not have {RESET}{old_email} {BLUE}Skipping...{RESET}"
        new_email = input(f"{BLUE}Please enter {GREEN}new{BLUE} email: {RESET}")
    record.change_email(old_email, new_email)
    return f"\n{GREEN}Email changed:\n  {RESET}{old_email} --> {new_email}"

@input_error
def delete_email(*args):
    ''' видалення емейла '''
    contact_name = name_request(*args)
    if contact_name not in list(address_book.data.keys()):
        raise KeyError
    record:Record = address_book.data[contact_name]
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
