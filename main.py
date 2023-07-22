import datetime
import requests
from contacts import Name, Phone, Record, AddressBook, Birthday
from decorators import input_error


API_KEY = "653c3ccd328356a16a58c6dbd440c093"
contacts = AddressBook()


def add_birthday(name, birthday):
    matching_names = [n for n in contacts if n.lower() == name.lower()]
    if matching_names:
        record = contacts[matching_names[0]]
        record.birthday = birthday
        return "Birthday added successfully"
    else:
        return "Contact not found"


@input_error
def add_contact(name, phone, birthday=None, address_book=None):
    name = Name(str(name).capitalize())
    if name.value in address_book:
        record = address_book[name.value]
        record.add_phone(phone)
        if birthday:
            record.birthday = birthday
    else:
        record = Record(name, phone, birthday)
        address_book.add_record(record)
    return "Contact added successfully"


@input_error
def change_contact(name, old_phone, new_phone):
    matching_names = [n for n in contacts if n.lower() == name.lower()]
    if matching_names:
        record = contacts[matching_names[0]]
        record.edit_phone(old_phone, new_phone)
        return "Contact updated successfully"
    else:
        return "Contact not found"


@input_error
def get_phone(name):
    matching_records = [record for record in contacts.values() if record.name.value.lower() == name.lower()]
    if matching_records:
        record = matching_records[0]
        return ", ".join([str(phone) for phone in record.phones])
    else:
        return "Contact not found"


def show_all_contacts():
    if contacts:
        output = ""
        for record in contacts.values():
            output += str(record)
        return output
    else:
        return "No contacts found"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The current weather in {city} is {weather_description}. Temperature: {temperature}°C"
    else:
        return "Failed to retrieve weather information"


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}"


def help_commands():
    return """
    Available commands:
    - hello: Greet the assistant
    - add <name> <phone> [birthday]: Add a contact with the given name, phone number, and optional birthday (in the format DD/MM)
    - change <name> <old_phone> <new_phone>: Change the phone number of an existing contact
    - phone <name>: Get the phone number(s) of a contact
    - show all: Show all saved contacts
    - weather <city>: Get the current weather in the specified city
    - time: Get the current time
    - save <filename>: Save the address book to a file
    - load <filename>: Load the address book from a file
    - search <query>: Search contacts by name or phone number
    - help: Show available commands
    - goodbye, close, exit: Close the assistant
    """


def parse_command(user_input, address_book):
    command = user_input[0]
    arguments = user_input[1:]

    if command == "hello":
        return "How can I help you?"
    elif command == "add":
        if len(arguments) >= 2:
            name = Name(" ".join(arguments[:-1]))
            phone = Phone(arguments[-1])
            if len(arguments) == 3:
                day, month = map(int, arguments[-1].split("/"))
                birthday = Birthday(day, month)
            else:
                birthday = None
            return add_contact(name, phone, birthday, address_book)
        else:
            raise ValueError("Give me name and phone please")
    elif command == "change":
        if len(arguments) == 3:
            name, old_phone, new_phone = arguments
            return change_contact(name, old_phone, new_phone)
        else:
            raise ValueError("Give me name, old phone, and new phone please")
    elif command == "phone":
        if len(arguments) == 1:
            name = " ".join(arguments)
            name = name.capitalize()
            return get_phone(name)
        else:
            raise ValueError("Enter user name")
    elif command == "show":
        if len(arguments) == 1 and arguments[0] == "all":
            return show_all_contacts(address_book)  
        else:
            raise ValueError("Invalid command. Type 'help'")
    elif command == "birthday":
        if len(arguments) >= 2:
            name = " ".join(arguments[:-1])
            date_str = arguments[-1]
            day, month = map(int, date_str.split("/"))
            birthday = Birthday(day, month)
            return add_birthday(name, birthday)
        else:
            raise ValueError("Give me name and birthday (in the format DD/MM) please")
    elif command == "weather":
        if len(arguments) == 1:
            city = arguments[0]
            return get_weather(city)
        else:
            raise ValueError("Enter city name")
    elif command == "time":
        return get_current_time()
    elif command == "help":
        return help_commands()
    elif command in ["good", "bye", "close", "exit"]:
         return "Good bye!"
    elif command == "save":
        if len(arguments) == 1:
            filename = arguments[0]
            address_book.save_to_file(filename)
            return f"Address book saved to {filename}"
        else:
            raise ValueError("Enter a filename to save the address book")

    elif command == "load":
        if len(arguments) == 1:
            filename = arguments[0]
            address_book = AddressBook.load_from_file(filename)
            return f"Address book loaded from {filename}"
        else:
            raise ValueError("Enter a filename to load the address book")

    elif command == "search":
        if len(arguments) == 1:
            query = arguments[0]
            search_results = address_book.search_records(query)
            if search_results:
                output = ""
                for record in search_results.values():
                    output += str(record)
                return output
            else:
                return "No matching contacts found"
        else:
            raise ValueError("Enter a search query")

    else:
        return "Invalid command. Type 'help' to see the available commands."


def main():
    address_book = AddressBook()
    print("Welcome to the Assistant! How can I help you?")
    while True:
        try:
            user_input = input("Enter a command: ").lower().split(" ")
            result = parse_command(user_input, address_book)  # Pass address_book to parse_command
            print(result)
            if result == "Good bye!":
                break
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()