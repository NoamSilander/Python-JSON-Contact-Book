import json
from pathlib import Path
import sys

#Continue working on searching and the boldness/italic codes implemented into searching
UNDERLINED = '\033[4m'
RESET = '\033[0m'
CONTACTS_FILE = Path('contacts.json')

def question_manager(question: str) -> str:
    contact_question = input(question)
    while True:
        user_confirm = input(f'Is {contact_question} correct? (y/n): ').lower().strip()
        match user_confirm:
            case 'y':
                return contact_question
            case 'n':
                contact_question = input(question)
            case _:
                pass

def file_create() -> str:
    if not CONTACTS_FILE.exists():
        print('Creating file...')
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f'Created {CONTACTS_FILE.name}')
        return 'new'
    else:
        print(f'Using existing {CONTACTS_FILE.name}')
        return 'old'

def file_init() -> None:
    not_valid = False
    status = file_create()
    if status == 'old':
        with open(CONTACTS_FILE, encoding='utf-8') as f:
            try:
                json.load(f)
            except json.JSONDecodeError:
                not_valid = True
        if not_valid:
            while True:
                user_choice = input('Not a valid JSON file! Would you like to wipe it? (y/n): ').lower().strip()
                match user_choice:
                    case 'y':
                        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
                            json.dump([], f)
                        print('Wiped!')
                        return
                    case 'n':
                        sys.exit('Please fix your JSON file and try again')
                    case _:
                        pass


def contact_manager() -> list:
    with open(CONTACTS_FILE, encoding='utf-8') as f:
        contacts = json.load(f)
    if not contacts:
        return contacts
    else:
        return contacts

def add_contact() -> dict:
    names = []
    contact_name = question_manager('Name: ')
    contact_name = contact_name.lower()
    for name in contact_name.split():
        capital_name = name.capitalize()
        names.append(capital_name)
    contact_name = ' '.join(names)
    while True:
        contact_email = question_manager('Email: ')
        if '@' in contact_email and '.' in contact_email:
            break
        print('Not a valid Email')
    while True:
        contact_number = question_manager('Phone: ')
        if not contact_number.isdigit():
            print('Phone number must only contain digits')
            continue
        if len(contact_number) < 4:
            print('Minimum length is four digits')
            continue
        break
    contact = {'Name': contact_name, 'Email': contact_email, 'Phone': contact_number}
    return contact
    
    

def list_contacts(contacts):
    if not contacts:
        print('No contacts added yet')
        return
    for i, person in enumerate(contacts, 1):
        print(f'{i}.{'-' * 19}')
        for category, value in person.items():
            print(f'{category}: {value}')
    input(f'{'-' * 20}\nEnter when done: ')

def search(contacts):
    if not contacts:
        print('Nothing to search from')
        return
    while True:
        user_search = input('What would you like to search for?: ').strip()
        if not user_search:
            print('Search must not be empty')
            continue
        for i, person in enumerate(contacts, 1):
            matches = False
            category_num = 0
            for category, value in person.items():
                category_num += 1
                if user_search in value:
                    underlined_word = value.replace(user_search, f'{UNDERLINED}{user_search}{RESET}')
                    print(f'{category}: {underlined_word}\nLocation: {i}, {category_num}')
                    matches = True
    if not matches:
        print('No matches')
        while True:
            user_continue = input('Would you like to keep searching? (y/n): ').lower().strip()
            match user_continue:
                case 'y':
                    break
                case 'n':
                    return
                case _:
                    pass

def main() -> None:
    file_init()
    contacts = contact_manager()
    while True:
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f)
        user_choice = input('\n--- Contact Book ---\n1. Add contact\n2. List contacts\n3. Search\n4. Delete contact\n5. Quit\n\nChoose (1-5): ').strip()
        match user_choice:
            case '1':
                contacts.append(add_contact())
            case '2':
                list_contacts(contacts)
            case '3':
                search(contacts)
            case '4':
                delete_contact()
            case '5':
                print('Quitting...')
                return
            case _:
                print('Please choose an option')

if __name__ == '__main__':
    main()