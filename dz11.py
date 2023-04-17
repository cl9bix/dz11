from datetime import datetime
from collections import UserDict

class Field:
    
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self):
        return str(self)
    

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self._validate_phone_number(value):
            raise ValueError("Invalid phone number format")

    def _validate_phone_number(self, value):
        # assume that the phone number must contain at least 7 digits and 
        # can have optional whitespace and dashes between the digits
        return len(''.join(filter(str.isdigit, value))) >= 7

    
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self._validate_birthday(value):
            raise ValueError("Invalid birthday format")

    def _validate_birthday(self, value):
        try:
            # assume that the birthday must be in YYYY-MM-DD format and a valid date
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Record:
    
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.birthday = None
        if birthday:
            self.set_birthday(birthday)
    
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))
    
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if str(phone) == phone_number:
                self.phones.remove(phone)
                return f'Phone number {phone_number} removed for contact {self.name}'
        return f'Phone number {phone_number} not found for contact {self.name}'

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if str(phone) == old_phone_number:
                phone.value = new_phone_number
                return f'Phone number {old_phone_number} updated to {new_phone_number} for contact {self.name}'
        return f'Phone number {old_phone_number} not found for contact {self.name}'
    
    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def days_to_birthday(self):
        if not self.birthday:
            return 'Birthday not set for contact'
        today = datetime.today()
        this_year_birthday = datetime.strptime(f'{today.year}-{self.birthday.value[5:]}', '%Y-%m-%d')
        if this_year_birthday < today:
            this_year_birthday = datetime.strptime(f'{today.year + 1}-{self.birthday.value[5:]}', '%Y-%m-%d')
        days_to_birthday = (this_year_birthday - today).days
        return days_to_birthday
    

class AddressBook(UserDict):

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
        records_str = '\n'.join(str(record) for record in self.data.values())
        return f'Address book:\n{records_str}'
    
    def show_all(self):
        return '\n'.join([str(rec) for rec in self.data.values()])  


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


def change(name, new_phone_number):
    if name in contacts:
        contacts[name] = new_phone_number
        return f'Phone number for user {name} is changed to {new_phone_number}.'
    else:
        return f'User with name: {name} is not found!'


def showall():
    # result = 'List of all contacts:\n'
    # for name, phone_number in contacts.items():
    #     result += f'{name}: {phone_number}\n'
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
            'show all': showall, 
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
