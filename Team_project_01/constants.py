RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

FILENAME = "book.bin"

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

README_TEXT = '''
    [92mThis is the CLI Address Book - an application that will simplify your work
    with contact information and save your time for more interesting cases.
    [94mUpdated and improved by "Bot farm " team.

    [92mWhen using command, note the following features:[94m
     * (required information to execute the command).
     * the input information should be separated by space.
     * Use date format "YYYY-MM-DD".
    [92mCommands to work with address book:[94m
        "hello" or "hi"     - greeting
        "help" or "?"       - calling for help
        "show all" or "all" - display all the contents of the phone book.
        "add phone" or "add"- (name and phone)  - add the phone to the contact. 
                              If the contact is missing create a new 
        "change phone" - (name, old phone, new phone) - edit phone record.
        "get contakt"  - (name) - show all contact information.
        "delete"       - (name) - delete a contact.
        "delete"       - (phone) - delete the phone.
        "load"         - loading of adpes book from file.
        "save"         - saving the address book to a file.
        "find"         - (string) search for matches in the address book, 
                         taking into account all contact fields
        "birthdays"    - (number of days) - show the contacts who have a birthday
                         in the coming days.
        "add email"    - (name and email) - add the email to the contact. 
                         If the contact does not exist, a new contact is created.
        "change email" - (name, old email and new email) - change email.
        "delete email" - (name) -  remove email from contact.
        "add adress"   - (name and address) - add address to contact.
        "change adress"- (name and new address) - change address.
        "delete adress"- (name and address) - delete adress from contact.
    [92mCommands to work with notes:[94m
        "add note"     - add notes.
        "add tags"     - add tags.
        "change note"  - change notes.
        "delete note" or "del note" - delete notes. 
        "delete tags" or "del tags" - remove tags.        
        "find note"    - find note.
        "sort notes"   - sort notes by tag.
    [92mCommand to organize files in a folder:[94m
        "sort folder" or "sort" - (name folder) - organize files in the specified folder
    [0m
    '''