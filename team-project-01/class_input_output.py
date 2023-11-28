from abc import ABC, abstractmethod
from functools import wraps
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from team-project-01.constants import RED, BLUE, GREEN, RESET

# class GeneratorHandler():
#     @wraps(func)
#     def wrapper(self, *args, **kwargs)
#         ...
#         # process generator
#         result = func(*args, **kwargs)



class AbstractInOut(ABC):
    @abstractmethod
    def output(self, text: str, *args):
        raise NotImplementedError

    @abstractmethod
    def input(self, *args, prompt: str = "?") -> str:
        raise NotImplementedError

    @abstractmethod
    def confirm(self, question: str) -> bool:
        raise NotImplementedError

class Console(AbstractInOut):
    ''' Output to terminal console '''
    def output(self, text: str, *args) :
        print(text)

    def input(self, *args, prompt: str = "?") -> str:
        if args:
            entered = args[0].strip()
        else:
            entered = input(f'{BLUE}{prompt}:{RESET} ').strip()
        return entered

    def confirm(self, question: str) -> bool:
        yes_no = f"{GREEN}[y]{RESET}es/{GREEN}[n]o: "
        try:
            confirmation = input(f'{RED}{question} {yes_no}').strip()
            if confirmation in 'yY':
                return True
            else:
                return False
        except KeyboardInterrupt:
            self.output('\n')
            return False

    def hinted_input(self, command_hints):
        ''' input with prompt_toolkit hints '''        
        command_completer = WordCompleter(command_hints, sentence=True, ignore_case=True)
        result = prompt(">>> ", completer=command_completer)
        return result

class Email(AbstractInOut):
    ''' Output to email '''
    def output(self, text: str, *args):
        ...

    def input(self, text: str, *args) -> str:
        ...

    def confirm(self, *args, prompt: str) -> bool:
        ...

class Telegram(AbstractInOut):
    ''' Output to Telegram '''
    def output(self, text: str, *args):
        ...

    def input(self, text: str, *args) -> str:
        ...

    def confirm(self, *args, prompt: str) -> bool:
        ...