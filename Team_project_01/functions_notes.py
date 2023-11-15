from Team_project_01.constants import RED, BLUE, GREEN, RESET
from Team_project_01.functions_common import input_error, yes_no


@input_error
def add_note():
    note = input(f"{BLUE}Please enter new note: {RESET}")
    if not note:
        if not yes_no(f'Are you sure you want to save blank note?'):
            return f"{GREEN}Note was {RED}not{GREEN} saved.{RESET}"
    note_rec = NoteRecord(note)
    tags = input(f"{BLUE}Please enter note tags: {RESET}")
    note_rec.add_tags(tags.split(", ") if "," in tags else tags.split(" "))
    add_record(note_rec)
    save_notes()
    return f"{GREEN}The note was saved.{RESET}"

@input_error
def find_note():
    find_func = input(f"Select search by {GREEN}[t]{RESET}ags or {GREEN}[n]{RESET}otes.")
    if find_func in "tags":
        use_func = find_by_tag
    elif find_func in "notes":
        use_func = find_by_note
    else:
        return f"{RED}You must choose: search by tags or notes!{RESET}"
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
        indx = input("{BLUE}Please enter the number of the note you want to edit: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    return found_notes, indx

@input_error
def change_note():
    found_notes, indx = find_note_to_func()
    changed_note = input(f"{BLUE}Please enter the note to change: {RESET}")
    if not changed_note:
        if not yes_no(f'Do you want save a blank note?'):
            return f"{GREEN}Note was {RED}not{GREEN} changed.{RESET}"
    found_notes[int(indx)-1].edit_note(changed_note)
    return f"{GREEN}The note was changed.{RESET}"

@input_error
def add_tags():
    found_notes, indx = find_note_to_func()
    new_tags = input(f"{BLUE}Please enter the tags you want to add: {RESET}")
    found_notes[int(indx)-1].add_tags(new_tags.split(", ") if "," in new_tags else new_tags.split(" "))
    return f"{GREEN}Tags were added.{RESET}"

@input_error
def delete_tags():
    found_notes, indx = find_note_to_func()
    tags_to_del = input(f"{BLUE}Please enter the tags you want to delete: {RESET}")
    found_notes[int(indx)-1].del_tags(tags_to_del.split(", ") if "," in tags_to_del else tags_to_del.split(" "))
    return f"{GREEN}Done.{RESET}"

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
        indx = input(f"{BLUE}Please enter the number of the note you want to delete: {RESET}")
    elif len(found_notes) == 1:
        indx = 1
    print(found_notes[int(indx)-1])
    check = input(f"{RED}Are you sure you want to delete this entry? {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
    if not check.lower() == "y":
        return f"{GREEN}Note was {RED}not{GREEN} deleted.{RESET}"
    delete_note(found_notes[int(indx)-1])
    return f"{GREEN}Note was deleted.{RESET}"
