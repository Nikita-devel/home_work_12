import datetime
import requests
import pickle


class Field:
    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __str__(self):
        return str(self._value).capitalize()


class Phone(Field):
    def __str__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

    @staticmethod
    def _is_valid_phone(phone):
        if len(phone) != 10:
            return False
        if not phone.isdigit():
            return False
        return True


class Birthday(Field):
    def __str__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_birthday(new_value):
            raise ValueError("Invalid birthday")
        self._value = new_value

    @staticmethod
    def _is_valid_birthday(birthday):
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
            return True
        except ValueError:
            return False



class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None

    def __str__(self):
        output = f"Name: {self.name.value}\n"
        for phone in self.phones:
            output += f"Phone: {phone.value}\n"
        output += "---------\n"
        return output


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def delete_record(self, record):
        self.records.remove(record)

    def edit_record(self, old_record, new_record):
        if old_record in self.records:
            index = self.records.index(old_record)
            self.records[index] = new_record

    def search_records(self, query):
        search_results = AddressBook()
        for record in self.records:
            if query.lower() in record.name.value.lower():
                search_results.add_record(record)
        return search_results

    def save_to_file(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)


API_KEY = "653c3ccd328356a16a58c6dbd440c093"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter both name and phone"

    return inner


contacts = AddressBook()
contacts.save_to_file("contacts.pickle")


@input_error
def add_contact(name, phone):
    name = Name(str(name).capitalize())
    phone = Phone(phone)
    if any(record.name.value == name.value for record in contacts.records):
        record = next((record for record in contacts.records if record.name.value == name.value), None)
    else:
        record = Record(name)
    record.add_phone(phone)
    if record not in contacts.records:
        contacts.add_record(record)
    return "Contact added successfully"


@input_error
def change_contact(name, old_phone, new_phone):
    record = next((record for record in contacts.records if record.name.value == name.value), None)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated successfully"
    else:
        return "Contact not found"


@input_error
def get_phone(name):
    record = next((record for record in contacts.records if record.name.value == name.value), None)
    if record:
        return record.phones
    else:
        return "Contact not found"


def show_all_contacts():
    if contacts.records:
        output = ""
        for record in contacts.records:
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
    - add <name> <phone>: Add a contact with the given name and phone number
    - change <name> <old_phone> <new_phone>: Change the phone number of an existing contact
    - phone <name>: Get the phone number(s) of a contact
    - show all: Show all saved contacts
    - weather <city>: Get the current weather in the specified city
    - time: Get the current time
    - help: Show available commands
    - goodbye, close, exit: Close the assistant
    """


def parse_command(user_input):
    command = user_input[0]
    arguments = user_input[1:]

    if command == "hello":
        print("How can I help you?")
    elif command == "add":
        if len(arguments) >= 2:
            name = Name(" ".join(arguments[:-1]))
            phone = Phone(arguments[-1])
            print(add_contact(name, phone))
        else:
            raise ValueError("Give me name and phone please")
    elif command == "change":
        if len(arguments) == 2:
            name, phone = arguments
            print(change_contact(name, phone))
        else:
            raise ValueError("Give me name and phone please")
    elif command == "phone":
        if len(arguments) == 1:
            name = arguments[0]
            try:
                print(get_phone(name))
            except KeyError:
                print("Contact not found")
        else:
            raise ValueError("Enter user name")
    elif command == "show":
        if len(arguments) == 1 and arguments[0] == "all":
            print(show_all_contacts())
        else:
            raise ValueError("Invalid command. Type 'help' to see the available commands.")
    elif command == "weather":
        if len(arguments) == 1:
            city = arguments[0]
            print(get_weather(city))
        else:
            raise ValueError("Enter city name")
    elif command == "time":
        print(get_current_time())
    elif command == "help":
        print(help_commands())
    elif command in ["good", "bye", "close", "exit"]:
        print("Good bye!")
        contacts.save_to_file("contacts.pickle")
        return True
    else:
        print("Invalid command. Type 'help' to see the available commands.")

    return False

def main():
    print("Welcome to the Assistant! How can I help you?")
    contacts = AddressBook.load_from_file("contacts.pickle")
    while True:
        try:
            user_input = input("Enter a command: ").lower().split(" ")
            if parse_command(user_input):
                break
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main()
