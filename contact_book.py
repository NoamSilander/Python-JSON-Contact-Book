import json
from pathlib import Path

CONTACTS_FILE = Path('contacts.json')

def file_init():
    if not CONTACTS_FILE.exists():
        print('Creating file...')
        CONTACTS_FILE.touch()
        print(f'Created {CONTACTS_FILE.name}')
        return 'new'
    else:
        print(f'Using existing {CONTACTS_FILE.name}')
        return 'old'

def load_list():
    contacts = []
    with open('contacts.json', 'a+', encoding='utf-8') as f:
        json.dump(contacts, f)
        try:
            json.load(f)
        except json.JSONDecodeError:
            while True:
                user_wipe = input('Not a valid JSON file. Would you like to wipe it? (y/n): ').lower().strip()
                match user_wipe:
                    case y:

def add_contact():
    with open('contacts.json', encoding='utf-8') as f:
        pass
def main() -> None:
    load_list()
    while True:
        user_choice = input('--- Contact Book ---\n1. Add contact\n2. List contacts\n3. Search\n4. Delete contact\n5. Quit\n\nChoose (1-5): ').strip()
        match user_choice:
            case '1':
                add_contact()
            case '2':
                list_contacts()
            case '3':
                search()
            case '4':
                delete_contact()
            case '5':
                print('Quitting...')
                return
            case _:
                print('Please choose an option')

if __name__ == '__main__':
    main()