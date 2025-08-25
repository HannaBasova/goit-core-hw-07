from collections import UserDict
from datetime import datetime,date,timedelta
from birthday import adjust_for_weekend,find_next_weekday, date_to_string






class Field:
    def __init__(self,value):
        self.value = value

    def __str__ (self):
        return str(self.value)

class Name(Field):
    def __init__(self,value:str):
        if value.strip() == '' or len(value) <= 1:
            raise ValueError ('Name should be real')
        super().__init__(value)

class Phone(Field):
    def __init__(self,value:str):#Має валідацію формату (10 цифр)
        if not value.isdigit()  or len(value) != 10:
            raise ValueError("Phone should consists of 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self,value:str): #22.05.2002
        try:
            date_obj = datetime.strptime(value,"%d.%m.%Y").date()
            super().__init__(date_obj)
            #Це поле не обов'язкове, але може бути тільки одне.
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self,name:str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self,phone:str):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self,phone:str):
        for item in self.phones:
            if phone == item.value:
                self.phones.remove(item)

    def edit_phone(self,old_phone:str, new_phone:str):
        for i, item in enumerate(self.phones):
            if old_phone == item.value:
                self.phones[i] = Phone(new_phone)

    def find_phone(self,phone)-> Phone | None:
        for item in self.phones:
            if item.value == phone:
                return item
        else:
            return None

    def add_birthday(self, birthday:str):
        if self.birthday is not None:
            return f"Birthday already exists"
        self.birthday = Birthday(birthday)
        return "Birthday added"

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def __str__(self):
        if not self.data:
            return f"Address Book is empty "
        else:
           return '\n'.join(str(record) for record in self.data.values())

    def add_record(self,record:Record):
        self.data[record.name.value] = record

    def find(self,name:str):
        return self.data.get(name)

    def delete(self,name:str):
        if name in self.data:
            del self.data[name]
        else:
            return f"Contact '{name}' not found"

    def get_upcoming_birthdays(self,days =7):
        upcoming_birthdays = []
        today = date.today()
        for item in self.data.values():
            birthday_this_year = item.birthday.value.replace(year=today.year)
            if  birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = adjust_for_weekend(birthday_this_year)
                congratulation_date_str = date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": item.name.value, "congratulation_date": congratulation_date_str})
                if upcoming_birthdays:
                    return '\n'.join(f"Contact: {item['name']} - congratulate on {item['congratulation_date']}" for item in upcoming_birthdays)
#[{'name': 'anna', 'congratulation_date': '01.09.2025'},
# {'name': 'ivan', 'congratulation_date': '29.08.2025'}]


