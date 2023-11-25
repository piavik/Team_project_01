from types import GeneratorType
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from Team_project_01.classes import Bot
# from Team_project_01.notes import *

from Team_project_01.constants import *



# def input_error(func):
#     ''' 
#     returns FUNCTION, not string !!!
#     '''
#     def inner(*args):
#         try:
#             result = func(*args)
#         except KeyError:
#             result = "Not found."
#         except ValueError:
#             result = "Entered incorrect data."
#         except IndexError:
#             result = "Not enough parameters."
#         except TypeError:
#             result = "Sorry, I do not understand."
#         else:
#             return result
#         return f'{RED}{result}{RESET}'
#     return inner

def _name_request(*args) -> str:
    return args[0].strip() if args else input(f"{BLUE}Please enter the contact name: {RESET}").strip()


def main() -> None:
    ''' main cycle'''
    # file_name = restore_data_from_file()
    # entered_file_name = input(f"From what file info should be fetched 
    # (default is '{FILENAME}')? ").lower()
    #file_name = FILENAME if entered_file_name == '' else entered_file_name
    file_name = FILENAME
    bot = Bot()
    # address_book = AddressBook()
    # address_book.load(file_name)
    # notes = Notes()
    # notes.load()
    command_hints = bot.commands.keys()
    command_completer = WordCompleter(command_hints, sentence=True, ignore_case=True)

    while True:
        input_ = prompt(">>> ", completer=command_completer)
        input_ = input_.strip()
        # check if user want to stop, strip() - just in case :)
        if input_.lower() in STOP_WORDS:
            # TODO: format dependent
            bot.address_book.save(file_name)
            bot.notes.save()
            print(f"{GREEN}See you, bye!{RESET}")
            break
        # check for empty input, do nothing
        if not input_:
            continue
        # simple split() does not allow to use spaces in commands dict
        command, parameters = bot.parse(input_)
        # all -> generator
        # other commands -> str
        result = command(*parameters)
        if isinstance(result, GeneratorType):
            for _selection in result:
                for _entry in _selection:
                    print(_entry)
                    print('----------')
                try:
                    brk = input(f"{RESET}....Press {BLUE}Enter{RESET} to continue, or {BLUE}'q'{RESET} to stop....\n")
                    if brk.lower() == 'q':
                        break
                except KeyboardInterrupt:
                    break
        elif isinstance(result, list):
            for rec in result:
                print(rec)
        else:
            print(f'{RESET}{result}')

if __name__ == "__main__":
    # locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    main()
