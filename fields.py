from datetime import datetime


class Field:
    ''' Базовий клас для полів запису '''
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return str(self.__value)

class Name(Field):
    ''' Клас для зберігання імені контакту. '''
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value) -> None:
        self.__value = value

class Phone(Field):
    ''' Клас для зберігання номера телефону. '''
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        ''' Вбудована перевірка, має бути 10 цифр '''
        PHONE_LENGTH = 10
        if not any([len(new_value) == PHONE_LENGTH, new_value.isdigit()]):
            raise ValueError
        self.__value = new_value

class Birthday(Field):
    ''' Клас для зберігання дня народження. '''
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_date: str) -> str:
        '''
        Вбудована перевірка, має бути правильний формат дати YYYY-MM-DD
        '''
        # TODO: Перевіряємо декілька варіантів формату дати:
        self.__value = datetime.strptime(new_date, '%Y-%m-%d').date()


    def __str__(self):
        return datetime.strftime(self.__value, '%d %B')
    
class Adress(Field):
    ''' Клас для зберігання адреси контакту. '''
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value) -> None:
        self.__value = value
