import json
from pathlib import Path
import sys
CONTACTS_FILE = Path('contacts.json')

def file_create():
    if not CONTACTS_FILE.exists():
        print('Creating file...')
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f'Created {CONTACTS_FILE.name}')
        return 'new'
    else:
        print(f'Using existing {CONTACTS_FILE.name}')
        return 'old'

def file_init():
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


def add_contact():
    with open('contacts.json', encoding='utf-8') as f:
        pass
def main() -> None:
    file_init()
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