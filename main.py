from my_classes import AddressBook
from handlers import parse_input,add_contact,change_contact,phone_username,show_all_contacts, add_birthday, show_birthday,birthdays, save_data,load_data

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    COMMANDS  = """
    1) "close" or "exit" - to exit from Bot
    2) "add [name] [phone]" - to add contact (example: add Anna 0931112233)
    3) "change [name] [old_phone] [new_phone] - to change phone (example: change Anna 0931112233 1234567890)
    4) "phone [name]" - to see the phone of contact (example: phone Anna)
    5) "all" - to print all contacts
    6) "add-birthday [name] [birthday]"  - to add birthday ihfo  to contact  (example: add-birthday Anna 22.12.1999)
    7) "show-birthday [name]" -  to see the birthday of contact ( example: show-birthday Anna)
    8) "birthdays" -  to see all birthdays in the next 7 working days
    """
    print(COMMANDS)
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args,book))

        elif command == "phone":
            print(phone_username(args,book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args,book))

        elif command == "show-birthday":
            print(show_birthday(args,book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
