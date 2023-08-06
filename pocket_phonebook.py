import os
from colorama import init, Fore
from sanitaze_phone_number import sanitaze_phone_number as sphn

phonebook = {}


def handler_com_hello(*args):
    init(autoreset = True)
    print("Hi.\nCan I " + Fore.YELLOW + "[help]" + "You?")


def handler_com_add(name: str, phone: str, *args):
    if name not in phonebook:
        phonebook[name] = phone
    print(f"Contact {name} with number {phone} was successfully added.")


def handler_com_change(name: str, phone: str, *args):
    if name in phonebook:
        phonebook[name] = phone
    print(f"Contact {name} with number {phone} was successfully changed.")


def handler_com_phone(name: str, *args):
    if name in phonebook:
        print(f"Your contact {name} has a number: {phonebook[name]}")

def handler_com_showall(*args):
    for name, phone in sorted(phonebook.items()):
        print("{:<18} -> {:<13}".format(name, phone))


def handler_com_help(*args):
    init(autoreset = True)
    introduse = "This is pocket phonebook.\n" \
                "For exit write [\"close\", \"exit\", \"goodbye\"].\n" \
                "Available commands [\"add Name Phone\", \"change Name Phone\",\n" \
                "\"hello\", \"help\", \"phone Name\", \"showall\"]."
    print(Fore.YELLOW + introduse)


def handler_com_exit(*args):
    if len(phonebook) > 0:
        file_store = "phonebook.txt"
        with open(file_store, "w") as file:
            for name, phone in phonebook.items():
                file.write(f"{name};{phone}\n")
        init(autoreset = True)
        print(Fore.YELLOW + "All data of this session are saved to a file " + Fore.BLUE + file_store + Fore.YELLOW + "\nGood bye!")        
    else:
        init(autoreset = True)
        print(Fore.YELLOW + "Good bye!")


COMMANDS = {'add': handler_com_add, 'change': handler_com_change,\
            'close': handler_com_exit, 'exit': handler_com_exit,\
            'goodbye': handler_com_exit, 'hello': handler_com_hello,\
            'help': handler_com_help,'phone': handler_com_phone,\
            'showall': handler_com_showall}


def input_error(get_handler):
    def wrapper(*args, **kwargs):
        try:
            return get_handler(*args, **kwargs)
        except KeyError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Key Error.\n" \
                  "Wrong command. Please, enter the correct Command.")
        except ValueError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Value Error. \n" \
                  "Invalid command parameters. Please, enter valid Name or Phone.")
        except IndexError:
            init(autoreset = True)
            print(Fore.YELLOW + "Oops! Index Error.\n" \
                  "Command parameters are missing. Please, enter correct parameters.")
    return wrapper


def command_parser(command_input: str) -> tuple:
    command_split = command_input.strip().split()
    if len(command_split) == 1:
        command = command_split[0].lower()
        return command, None, None
    elif len(command_split) == 2:
        command = command_split[0].lower()
        name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
        return command, name, None
    elif len(command_split) == 3:
        command = command_split[0].lower()
        name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
        phone = command_split[2] if len(command_split[2]) >= 10 else None
        sanitazed_phone = sphn(phone)
        return command, name, sanitazed_phone
    # command = command_split[0].lower() if len(command_split[0]) > 0 else None
    # name = command_split[1].lower().title() if len(command_split[1]) > 2 else None
    # phone = command_split[2] if len(command_split[2]) >= 10 else None
    # return command, name, phone


@input_error
def get_handler(command: str, name: str, phone: str):
    # command, name, phone = command_parser(command_input)
    if command not in COMMANDS:
        raise KeyError
    elif command in ("add", "change") and (name is None or phone is None):
        raise IndexError
    elif command == "phone" and name is None:
        raise IndexError
    elif command in ("add", "change") and not (name.isalpha() and phone.isdigit() and len(phone) >= 10):
        raise ValueError
    elif command in ("change", "phone") and name not in phonebook:
        raise ValueError
    else:
        return COMMANDS[command](name, phone)


def main():
    if os.path.exists("phonebook.txt"):
        with open("phonebook.txt", "r", encoding = "UTF-8") as file:
            for line in file:
                name, phone = line.strip().split(';')
                phonebook[name] = phone
    

    init(autoreset = True)
    let_begin = "Please, choose command \"help\" for begin"
    print(Fore.YELLOW + let_begin)
        
    while 1:
        command_input = input("Common your command: ")
        if not command_input:
            continue
        command, name, phone = command_parser(command_input)
        get_handler(command, name, phone)
        if command in ("exit", "close", "goodbye"):
            break


if __name__ == "__main__":  
    main()