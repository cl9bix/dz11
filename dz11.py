from collections import UserDict
from datetime import date
import datetime
contacts = {}

class Field:
    
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self._value = value
    
    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self):
        return str(self)
    
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self._value = value

    
class Name(Field):
    pass

class Phone(Field):
    
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit():
            raise ValueError("Phone number must be a string of digits only")

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False
    
class Record:
    
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = {phone.value} if phone else set()
        if birthday:
            try:
                birthday_date = date.fromisoformat(birthday.value)
                if birthday_date.year < 1900 or birthday_date.year > date.today().year:
                    raise ValueError("Invalid birthday year")
                self.birthday = birthday_date
            except ValueError:
                raise ValueError("Invalid birthday format. Use ISO format 'YYYY-MM-DD'")
        else:
            self.birthday = None
    
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = date.today()
        next_birthday = date(today.year, self.birthday.month, self.birthday.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birthday.month, self.birthday.day)
        return (next_birthday - today).days
        

    def add_phone(self, phone_number):
        if not isinstance(phone_number, Phone):
            phone_number = Phone(phone_number)
        self.phones.add(phone_number.value)
        return f'Contact with name: {self.name} is added!'

    def remove_phone(self, phone_number):
        if phone_number in self.phones:
            self.phones.remove(phone_number)
            return f'Contact with name: {self.name} removed!'
        return f'Phone number {phone_number} not found for contact {self.name}'

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if str(phone) == old_phone_number:
                new_phone = Phone(new_phone_number)
                self.phones.add(new_phone.value)
                return f'Phone number {old_phone_number} updated to {new_phone_number} for contact {self.name}'
            return f'Phone number {old_phone_number} not found for contact {self.name}'
    

    def __str__(self):

        return f'Name: {self.name}\nPhones:\n{",".join(self.phones)}'


class Birthday(Field):
    def __init__(self, value=None):
        if value is not None and not isinstance(value, datetime.date):
            raise ValueError("Value must be a date object")
        self.value = value
    def __init__(self, value):
        super().__init__(value)
        self.date = None
        try:
            self.date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format, should be YYYY-MM-DD")

    def __eq__(self, other):
        if isinstance(other, Birthday):
            return self.date == other.date
        return False

    def __str__(self):
        return str(self.date)

    @property
    def value(self):
        return str(self.date)

    @value.setter
    def value(self, value):
        try:
            self.date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format, should be YYYY-MM-DD")    

class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = 5  # кількість записів на сторінці

    def add_record(self, record):
        self.data[record.name.value] = record
        return f'Contact {record.name} added to the address book!'

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
            return f'Contact {name} removed from the address book!'
        return f'Contact {name} not found in the address book!'

    def find_record(self, name):
        if name in self.data:
            return str(self.data[name])
        return f'Contact {name} not found in the address book!'

    def __str__(self):
        return 'Address book:\n' + '\n'.join(str(record) for record in self.data.values())

    def show_all(self):
        curent_index = 0  
        records = list(self.data.values())
        while curent_index < len(records):
            page_records = records[curent_index:curent_index+self.page_size]
            for record in page_records:
                yield str(record)
            curent_index += self.page_size


contacts = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Print help"
    return inner


@input_error
def add_contact(name, phone_number):
    
    contacts.add_record(Record(Name(name), Phone(phone_number)))


def phone(name):
    rec = contacts.get(name)
    if rec:
        return f'Phone number for user {name}: {rec.phones}'
    else:
        return f'Contact with name: {name} is not found!'


def change(*args):

    name = Name(args[0])
    old_phone = args[1]
    new_phone = args[2]
    if name.value not in contacts.keys():
        return f"Contact {name.value} not found"
    if old_phone not in contacts[name.value].phones:
        return f"Phone {old_phone} not found for {name.value}"
    if new_phone in contacts[name.value].phones:
        return "Phone already in list"
    contacts[name.value].phones.remove(old_phone)
    contacts[name.value].phones.add(new_phone)

    return f"Contact {name.value} with phone number {old_phone} was updated with new phone number {new_phone}"

    
@input_error
def add_phone(name, phone_number):
    if name not in contacts:
        return f'Contact {name} not found in the address book!'
    contacts[name].phones.add(phone_number)
    return f"New phone number {phone_number} added to the contact {name}"
    

def showall():

    return contacts.show_all()


def hello(*args):
    return 'How can I help you?'


def close_bot(*args):
    return 'Goodbye!'


def no_command(*args):
    return 'Unknown command, try again!'


COMMANDS = {'hello': hello,
            'add': add_contact,
            'change': change,
            'phone': phone,
            'new number': add_phone,
            'show all': showall,
            'birthday': days_to_birthday,
            'goodbye': close_bot,
            'close': close_bot, 
            'exit': close_bot 
            }



def command_handler(text):
    for kword, command in COMMANDS.items():
        if text.startswith(kword):
            return command, text.replace(kword, '').strip()
    return no_command, None


def main():
    while True:
        user_input = input('>>>')
        command, data = command_handler(user_input)
        if command == exit:
            print(command())
            break
        elif command == no_command:
            print(command())
        elif data is not None:
            result = command(*data.split())
            if result:
                print(result)
        else:
            result = command()
            if result:
                print(result)


if __name__ == '__main__':
    main()
