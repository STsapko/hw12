from collections import UserDict
from datetime import datetime, date
import pickle

class Field:

    def __init__(self,value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass

class EMail(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone
    
    @phone.setter
    def phone(self, value):
        try:
             int(value)
        except:
            raise ValueError('Must contain only numbers')
        self.__phone = value

    def __str__(self) -> str:
        return str(self.__phone)

class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    def birthday(self, value):
        try:
             datetime.strptime(value, '%Y-%m-%d').date()
        except:
            raise ValueError(f'birthday has to be in yyyy-mm-dd format')
        self.__birthday = value

    def __str__(self) -> str:
        return str(self.__birthday)


class Record:

    def __init__(self, 
                 name: Name, 
                 email: EMail=None, 
                 phone: Phone=None,
                 birthday: Birthday = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if old_phone.phone in [ph.phone for ph in self.phones]:
            self.phones = [ph if ph.phone != old_phone.phone else new_phone for ph in self.phones]

    def delete_phone(self, phone_to_del: Phone):
        if phone_to_del.phone in [ph.phone for ph in self.phones]:
            self.phones = [ph for ph in self.phones if ph.phone != phone_to_del.phone]
            
    def add_email(self, email: EMail):
        self.email = email

    def change_email(self, new_email: EMail):
        self.email = new_email

    def delete_email(self):
        self.email = None

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            birthday_date = datetime.strptime(str(self.birthday), '%Y-%m-%d').date()
            if birthday_date.month == 2 and birthday_date.day == 29:
                birthday_this_year = datetime(datetime.now().year, 3, 1).date()
            else:
                birthday_this_year = datetime(datetime.now().year, birthday_date.month, birthday_date.day).date()
            return (birthday_this_year - date.today()).days if (birthday_this_year - date.today()).days >= 0 else 365 + (birthday_this_year - date.today()).days
        return None

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, page=1):
        start = 0
        while True:
            result_keys = list(self)[start:start+page]
            result = [self.data.get(k) for k in result_keys]
            if not result:
                break
            yield result
            start += page

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)


if __name__ == "__main__":
    pass
    name = Name('a')
    record = Record(name, birthday=Birthday('1979-06-12'))
    record.add_phone(Phone(1))
    record.add_phone(Phone(2))
    record.add_phone(Phone(3))
    record.delete_phone(Phone(1))
    record.change_phone(Phone(3), Phone(4))
    print(record.name, [ph.phone for ph in record.phones])
    print(Phone(3).phone in [ph.phone for ph in record.phones])
    print(Phone(4).phone in [ph.phone for ph in record.phones])
    print(Phone(3))
    print([ph.phone for ph in record.phones])
    record.add_birthday(Birthday('1979-12-06'))
    # print(record.name, record.birthday)
    print(record.birthday)
    # record.add_birthday(Birthday('19790612'))
    # print(record.name, record.birthday)
    print(record.days_to_birthday())
    record.add_birthday(Birthday('1946-03-30'))
    print(record.days_to_birthday())
