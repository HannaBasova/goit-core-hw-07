from datetime import timedelta
from my_classes import Record,AddressBook
import pickle

COMMANDS = """
   1) "close" or "exit" - to exit from Bot
   2) "add [name] [phone]" - to add contact (example: add Anna 0931112233)
   3) "change [name] [old_phone] [new_phone] - to change phone (example: change Anna 0931112233 1234567890)
   4) "phone [name]" - to see the phone of contact (example: phone Anna)
   5) "all" - to print all contacts
   6) "add-birthday [name] [birthday]"  - to add birthday ihfo  to contact  (example: add-birthday Anna 22.12.1999)
   7) "show-birthday [name]" -  to see the birthday of contact ( example: show-birthday Anna)
   8) "birthdays" -  to see all birthdays in the next 7 working days
   """
def parse_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError:
            print(COMMANDS)
            return None, []
    return inner

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as e:
            return str(e)
        except AttributeError:
            print(f"Contact not found")
    return inner

@parse_error
def parse_input(user_input):
    command, *args = user_input.lower().strip().split()
    return command, args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact changed"
    record.edit_phone(old_phone,new_phone)
    return message

@input_error
def phone_username(args,book:AddressBook)-> str|None: #phones by name
    name, *_ = args
    record = book.find(name)
    return '\n'.join(f"Phone: {phone.value}" for phone in record.phones)

def show_all_contacts(book:AddressBook):
    return(book)

@input_error
def add_birthday(args,book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    return record.add_birthday(birthday)

@input_error
def show_birthday(args,book):
    name, *_ = args
    record = book.find(name)
    if record.birthday:
        return f"Birthday of {name} is on {record.birthday.value}"
    else:
        return f'Birthday of {name} does not added'


def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(f"Contact : {item['name']} -  congratulation on :  {item['birthday']}" for item in upcoming)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


