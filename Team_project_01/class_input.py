from abc import ABC, abstractmethod


class AbstractInput(ABC):
    @abstractmethod
    def Input(self, text: str, *args) -> str:
        ...


class TerminalInput(AbstractInput):
    ''' Input from terminal console '''
    def __init_(self):
        ...

    def Input(self, text: str, *args) -> str:
        ...

class EmailInput(AbstractInput):
    ''' Input from email '''
    def __init_(self):
        ...

    def Input(self, text: str, *args) -> str:
        ...


class TelegramInput(AbstractInput):
    ''' Input from Telegram '''
    def __init_(self):
        ...

    def Input(self, text: str, *args) -> str:
        ...
