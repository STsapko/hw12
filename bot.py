from manage_address_book import AddressBook, Record, Name, Phone, EMail, Birthday


file_name = 'address_book.bin'
try:
    address_book = AddressBook.load_from_file(file_name)
except FileNotFoundError:
    address_book = AddressBook()
    address_book.save_to_file(file_name)

def help(*args):
    return \
"""menu:
    optional info*
    hello
    add contact  (name phone* email* birthday*)
    add phone    (name phone)
    change phone (name phone new_phone) 
    delete phone (name phone)
    add email    (name email)
    change email (name new_email)
    delete email (name)
    add birthday (name birthday)
    till birthday(name)
    search       (column (name or phone) search)
    show all     (pages*)
    exit (exit, close, good bye)
    """

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name and appropriate data please"
        except KeyError:
            return "No such name"
        except ValueError:
            return "Enter user name"
    return wrapper

def say_hello(*args):
    return 'How can I help you?'

def exit(*args):
    return 'Good bye!'

def no_command(*args):
    return "Unknown operation, try again."

@input_error
def add_contact(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    record = Record(name)
    phone = None
    try:
        phone = Phone(list_of_params[1])
        if phone:
            record.add_phone(phone)
    except IndexError:
        pass
    email = None
    try:
        email = EMail(list_of_params[2])
        if email:
            record.add_email(email)
    except IndexError:
        pass
    birthday = None
    try:
        birthday = Birthday(list_of_params[3])
        if email:
            record.add_birthday(birthday)
    except IndexError:
        pass    
    address_book.add_record(record) 
    return f"Contact {list_of_params[0]} added successfully"

@input_error
def add_phone(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    phone = Phone(list_of_params[1])
    contact: Record = address_book.get(name.value)
    if contact:
        contact.add_phone(phone)
        return f'Name: {name.value} tel {phone} is added'
    else:
        return f'No contact {name}'

@input_error
def delete_phone(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    phone = Phone(list_of_params[1])
    contact: Record = address_book.get(name.value)
    if contact:
        contact.delete_phone(phone)
        return f'Name: {name.value} tel {phone} is deleted'
    else:
        return f'No contact Name: {name.value}'

@input_error
def change_phone(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    old_phone = Phone(list_of_params[1])
    new_phone = Phone(list_of_params[2])
    contact: Record = address_book.get(name.value)
    if contact:
        if old_phone.phone in [ph.phone for ph in contact.phones]:
            contact.change_phone(old_phone, new_phone)
            return f'Name: {name.value} tel {old_phone} is changed to {new_phone}'
        else:
            return f'For Name: {name.value} no tel {old_phone}'
    else:
        return f'No contact {name}'

@input_error
def add_email(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    email = EMail(list_of_params[1])
    contact: Record = address_book.get(name.value)
    if contact:
        contact.add_email(email)
        return f'Name: {name.value} email {email.value} is added'
    else:
        return f'No contact {name}'
    
@input_error
def change_email(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    email = EMail(list_of_params[1])
    contact: Record = address_book.get(name.value)
    if contact:
        old_email = contact.email
        contact.change_email(email)
        return f'Name: {name.value} tel {old_email.value} is changed to {email.value}'
    else:
        return f'No contact {name}'

@input_error
def delete_email(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    contact: Record = address_book.get(name.value)
    if contact:
        old_email = contact.email
        contact.delete_email()
        return f'Name: {name.value} email {old_email.value} is deleted'
    else:
        return f'No contact {name}'
    
@input_error
def add_birthday(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    birthday = Birthday(list_of_params[1])
    contact: Record = address_book.get(name.value)
    if contact:
        contact.add_birthday(birthday)
        return f'Name: {name.value} birthday {birthday} is added'
    else:
        return f'No contact {name}'

# def show_all_contacts(*args):
#     result = ''
#     for record in address_book.values():
#         result += f"Name: {record.name}, phones: {'-' if not [ph.phone for ph in record.phones] else [ph.phone for ph in record.phones]}, email: {'-' if not record.email else record.email}, birthday: {'-' if not record.birthday else record.birthday}" +'\n'
#     if not result:
#         return 'No contacts yet'
#     return result

@input_error
def days_to_birthday(*args):
    list_of_params = args[0].split()
    name = Name(list_of_params[0])
    contact: Record = address_book.get(name.value)
    if contact:
        return f'Name: {name.value} - {contact.days_to_birthday()} days till the next birthday' if contact.days_to_birthday() else f'Name: {name.value} - no info with birthday yet'
    else:
        return f'No contact {name}'

@input_error
def search(*args):
    list_of_params = args[0].split()
    column = list_of_params[0]
    search = list_of_params[1]
    result = ''
    for record in address_book.values():
        if (column == 'name' and record.name.value.find(search)>=0) or (column == 'phone' and [ph.phone for ph in record.phones if ph.phone.value.find(search) >= 0]):
            result += f"Name: {record.name}, phones: {'-' if not [ph.phone for ph in record.phones] else [ph.phone for ph in record.phones]}, email: {'-' if not record.email else record.email}, birthday: {'-' if not record.birthday else record.birthday}" +'\n'
    return 'no matches' if not result else result

@input_error
def show_all_contacts(*args):
    if len(address_book) == 0:
        return 'No contacts yet'
    try:
        list_of_params = args[0].split()
        pages = int(list_of_params[0])
    except:
        result = ''
        for record in address_book.values():
            result += f"Name: {record.name}, phones: {'-' if not [ph.phone for ph in record.phones] else [ph.phone for ph in record.phones]}, email: {'-' if not record.email else record.email}, birthday: {'-' if not record.birthday else record.birthday}" +'\n'
        return result
    address_book_iterator = address_book.iterator(pages)
    for page in address_book_iterator:
        print("*"*40)
        result = ""
        for record in page:
            result += f"Name: {record.name}, phones: {'-' if not [ph.phone for ph in record.phones] else [ph.phone for ph in record.phones]}, email: {'-' if not record.email else record.email}, birthday: {'-' if not record.birthday else record.birthday}" +'\n'
        print(result)
        input('Press any key')
    return "*" * 40

OPERATIONS = {
    add_contact: 'add contact',
    add_phone: 'add phone',
    delete_phone: 'delete phone',
    change_phone: 'change phone',
    add_email: 'add email',
    delete_email: 'delete email',
    change_email: 'change email',
    add_birthday: 'add birthday',
    days_to_birthday: 'till birthday',
    show_all_contacts: 'show all',
    search: 'search',
    say_hello: 'hello',
    exit: ['exit', 'close','goodbye'],
}

def get_operation(text: str):
    for operation, kword in OPERATIONS.items():
        if type(kword) == str:
            if text.lower().startswith(kword):
                return operation, text[len(kword):].strip()
        if type(kword) == list:
            for k in kword:
                if text.startswith(k):
                    return operation, text[len(kword):].strip()
    return no_command, None
     
def main():
    print(help())
    while True:
        user_input = input('>>> ')
        operation, data = get_operation(user_input)
        print(operation(data))
        address_book.save_to_file(file_name)
        if operation == exit:
            break

if __name__ == '__main__':
    main()