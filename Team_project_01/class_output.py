from abc import ABC, 


class AbstractOutput(ABC):
    @abstractmethod
    def output(self, text: str, *args) -> str:
        ...


class TerminalOutput(AbstractOutput):
    ''' Output to terminal console '''
    def __init_(self):
        ...

    def output(self, text: str, *args) -> str:
        ...

class EmailOutput(AbstractOutput):
    ''' Output to email '''
    def __init_(self):
        ...

    def output(self, text: str, *args) -> str:
        ...


class TelegramOutput(AbstractOutput):
    ''' Output to email '''
    def __init_(self):
        ...

    def output(self, text: str, *args) -> str:
        ...
