import json
from pathlib import Path
import sys

UNDERLINED = '\033[4m'
RESET = '\033[0m'
SEPARATOR = '-' * 20
CONTACTS_FILE = Path('contacts.json')

def cap_words(text: str) -> str:
    words = []
    text = text.lower()
    for word in text.split():
        capital_text = word.capitalize()
        words.append(capital_text)
    capped_words = ' '.join(words)
    return capped_words

def ask_question(question: str, thing: str) -> str:
    while True:
        user_question = input(question).strip()
        if not user_question:
            print(f'{thing} must not be empty')
            continue
        return user_question
            
def ask_number_y_to_i(question: str, y: int, i: int) -> int:
    while True:
        try:
            contact_choice = int(input(f'{SEPARATOR}\n{question} ({y}-{i}): '))
        except ValueError:
            print('Choose a valid option')
            continue
        if contact_choice < y or contact_choice > i:
            print('Choose a valid option')
            continue
        return contact_choice
    

def question_manager(question: str, thing: str) -> str:
    contact_question = ask_question(question, thing)
    while True:
        user_confirm = input(f'Is {contact_question} correct? (y/n): ').lower().strip()

        match user_confirm:
            case 'y':
                return contact_question
            case 'n':
                contact_question = ask_question(question, thing)
            case _:
                pass

def contact_manager() -> list:
    with open(CONTACTS_FILE, encoding='utf-8') as f:
        contacts = json.load(f)
    if not contacts:
        return contacts
    else:
        return contacts

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

def replace_contact(contacts: list):
    for i, person in enumerate(contacts, 1):
        print(f'{i}. {person['Name']}')
    contact_choice = ask_number_y_to_i('Choose a contact', 1, i)
    for i, (key, value) in enumerate(contacts[contact_choice - 1].items(), 1):
        print(f'{i}. {key}: {value}')
    category_choice = ask_number_y_to_i('Choose what to replace', 1, i)
            

def add_contact() -> dict:
    names = []
    contact_name = question_manager('Name: ', 'Name')
    contact_name = cap_words(contact_name)
    while True:
        contact_email = question_manager('Email: ', 'Email')
        if '@' in contact_email and '.' in contact_email:
            break
        print('Not a valid Email')
    while True:
        contact_number = question_manager('Phone: ', 'Phone')
        if not contact_number.isdigit():
            print('Phone number must only contain digits')
            continue
        if len(contact_number) < 4:
            print('Minimum length is four digits')
            continue
        break
    contact = {'Name': contact_name, 'Email': contact_email, 'Phone': contact_number}
    return contact
    
    

def list_contacts(contacts: list) -> None:
    if not contacts:
        print('No contacts added yet')
        return
    for i, person in enumerate(contacts, 1):
        print(f'{i}.{'-' * 19}')
        for category, value in person.items():
            print(f'{category}: {value}')
    input(f'{SEPARATOR}\nEnter when done: ')

def search(contacts: list) -> None:
    matches = False
    if not contacts:
        print('Nothing to search from')
        return
    while True:
        user_search = ask_question(f'{SEPARATOR}\nWhat would you like to search for?: ', 'Search')
        for i, person in enumerate(contacts, 1):
            category_num = 0
            for category, value in person.items():
                category_num += 1
                user_search_capital = cap_words(user_search)
                if user_search in value:
                    underlined_word = value.replace(user_search, f'{UNDERLINED}{user_search}{RESET}')
                    print(f'{category}: {underlined_word}\nLocation: {i}, {category_num}')
                    matches = True
                elif user_search_capital in value:
                    underlined_word = value.replace(user_search_capital, f'{UNDERLINED}{user_search_capital}{RESET}')
                    print(f'{category}: {underlined_word}\nLocation: {i}, {category_num}\n{SEPARATOR}')
                    matches = True
        if not matches:
            print(f'{SEPARATOR}\nNo matches')
        while True:
            user_continue = input('Would you like to keep searching? (y/n): ').lower().strip()
            match user_continue:
                case 'y':
                    matches = False
                    break
                case 'n':
                    return
                case _:
                    pass

def delete_replace_manager(contacts: list):
    while True:
        user_choice = input(f'{SEPARATOR}\n1. Replace contact info\n2. Delete contact\n\nChoose (1-2): ').strip()
        match user_choice:
            case '1':
                replace_contact(contacts)
            case '2':
                delete_contact(contacts)
            case _:
                print('Please choose an option')


def main() -> None:
    file_init()
    contacts = contact_manager()
    while True:
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f)
        user_choice = ask_number_y_to_i(f'\n--- Contact Book ---\n1. Add contact\n2. List contacts\n3. Search\n4. Delete/Replace contact\n5. Quit\n{SEPARATOR}\nChoose', 1, 5)
        match user_choice:
            case 1:
                contacts.append(add_contact())
            case 2:
                list_contacts(contacts)
            case 3:
                search(contacts)
            case 4:
                delete_replace_manager(contacts)
            case 5:
                print('Quitting...')
                return

if __name__ == '__main__':
    main()