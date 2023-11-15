from Team_project_01.constants import RED, BLUE, GREEN, RESET


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
            result = "Entered incorrect data."
        except IndexError:
            result = "Not enough parameters."
        except TypeError:
            result = "Sorry, I do not understand."
        else:
            return result
        return f'{RED}{result}{RESET}'
    return inner

def name_request(*args) -> str:
    ''' Запит імені, якщо його немає в першому аргументі '''
    return args[0].strip() if args else input(f"{BLUE}Please enter the contact name: {RESET}").strip()

def yes_no(question: str) -> bool:
    ''' Запит користувача: так/ні '''
    res = input(f"{RED}{question} {GREEN}[y]{RESET}es/{GREEN}[n]{RESET}o: ")
    return False if not res.lower() == "y" else True
