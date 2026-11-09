import json

def file_init() -> None:
    try:
        with open('contacts.json', 'x', encoding='utf-8') as f:
            print('Created file')
    except FileExistsError:
        print(f'Using existing file')

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