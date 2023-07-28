# Contact Management Assistant

This is a simple command-line contact management assistant that allows users to manage contacts, add birthdays, get weather information, and more.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies using pip:

    pip install -r requirements.txt


3. Run the `main.py` script:

    python main.py


4. Follow the instructions provided by the assistant to manage contacts and utilize other features.

## Features

- Add new contacts with their name and phone number.
- Optionally, add a birthday to a contact.
- Change the phone number of an existing contact.
- Get the phone number(s) of a contact.
- Search for contacts by name or phone number.
- Show all saved contacts.
- Get the current weather in a specified city.
- Get the current time.

## How It Works

The assistant uses the OpenWeatherMap API to get weather information for a specific city. It also saves and loads contact data in a CSV file (`contacts.csv`). The assistant's features are implemented as separate functions in the `assistant.py` file, and contact management functionalities are provided through the `contacts.py` module.

## Contact Management

The `contacts.py` module contains classes representing contact details, such as `Name`, `Phone`, `Birthday`, and `Record`. The `AddressBook` class manages a collection of contacts and provides functionalities to add, edit, delete, and search contacts. The contact data is stored in a CSV file.

## Decorator

The `decorators.py` module contains the `input_error` decorator. This decorator handles errors related to contact management functions, such as KeyError, ValueError, and IndexError, and returns user-friendly error messages.

## Commands

Below are the available commands:

- `hello`: Greet the assistant.
- `add <name> <phone> [birthday]`: Add a contact with the given name, phone number, and optionally, the birthday (format: DD/MM).
- `change <name> <old_phone> <new_phone>`: Change the phone number of an existing contact.
- `phone <name>`: Get the phone number(s) of a contact.
- `search <query>`: Search contacts by name or phone number.
- `show all`: Show all saved contacts.
- `weather <city>`: Get the current weather in the specified city.
- `time`: Get the current time.
- `help`: Show available commands.
- `goodbye`, `close`, `exit`: Close the assistant.

## Note

Please note that the assistant uses the OpenWeatherMap API, and you need to provide your own API key (replace `API_KEY = "YOUR_API_KEY"` in the `assistant.py` script) to use the weather feature.

Feel free to explore, modify, and extend this assistant as needed!
