import datetime
import csv
import os
import datetime

# Class representing a Name, which has a value that is capitalized
class Name:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = str(new_value).capitalize()

    def __str__(self):
        return str(self._value)

# Class representing a Phone, which has a value that can be set and retrieved
class Phone:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)

# Class representing a Birthday, with day and month attributes
class Birthday:
    def __init__(self, day=None, month=None):
        self._day = day
        self._month = month

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, new_day):
        self._day = new_day

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, new_month):
        self._month = new_month

    def __str__(self):
        if self._day is None or self._month is None:
            return "Not specified"
        return f"{self._day:02d}/{self._month:02d}"

# Class representing a Record in the AddressBook
class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(str(name).capitalize())
        self.phones = []
        if phone is not None:
            self.phones.append(Phone(phone))
        self.birthday = birthday

    # Method to add a phone to the record
    def add_phone(self, phone):
        if phone not in self.phones:
            self.phones.append(phone)

    # Method to delete a phone from the record
    def delete_phone(self, phone):
        self.phones.remove(phone)

    # Method to edit a phone in the record
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found")

    # Method to calculate days remaining to the birthday
    def days_to_birthday(self):
        if self.birthday is None:
            return "Birthday not specified"
        
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, self.birthday.month, self.birthday.day)
        
        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, self.birthday.month, self.birthday.day)
        
        days_remaining = (next_birthday - today).days
        return days_remaining

    # Method to represent the record as a string
    def __str__(self):
        output = f"Name: {self.name.value}\n"
        output += f"Birthday: {self.birthday}\n"
        output += f"Phone: {', '.join(str(phone) for phone in self.phones)}\n"
        output += "---------\n"
        return output
    
# Class representing an AddressBook, which is a dictionary of Records
class AddressBook(dict):
    def __init__(self, filename="contacts.csv"):
        self.filename = filename
        self.page_size = 10
        if not os.path.isfile(filename):
            self.create_empty_csv_file()
        self.load_data()

    # Method to create an empty CSV file with header
    def create_empty_csv_file(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Name", "Phones", "Birthday"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    # Method to set the page size for pagination
    def set_page_size(self, size):
        self.page_size = size

    # Method to add a record to the address book
    def add_record(self, record):
        self[record.name.value] = record

    # Method to delete a record from the address book
    def delete_record(self, name):
        del self[name.value]

    # Method to edit a record in the address book
    def edit_record(self, name, new_record):
        self[name.value] = new_record

    # Method to search records in the address book based on query
    def search_records(self, query):
        search_results = AddressBook()
        for record in self.values():
            if query.lower() in record.name.value.lower() or query in record.phones:
                search_results.add_record(record)
        return search_results

    # Method to iterate over records in pages
    def iterator(self):
        records = list(self.values())
        total_pages = (len(records) + self.page_size - 1) // self.page_size

        for page_num in range(total_pages):
            start_idx = page_num * self.page_size
            end_idx = (page_num + 1) * self.page_size
            yield records[start_idx:end_idx]

    # Method to save the address book data to a CSV file
    def save_data(self, filename="contacts.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Name", "Phones", "Birthday"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for record in self.values():
                phones = ', '.join(str(phone) for phone in record.phones)
                birthday_day = record.birthday.day if record.birthday else ""
                birthday_month = record.birthday.month if record.birthday else ""
                writer.writerow({"Name": record.name.value, "Phones": phones, "Birthday": f"{birthday_day}/{birthday_month}"})

    # Method to load the address book data from a CSV file
    def load_data(self, filename="contacts.csv"):
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["Name"]
                phones = row["Phones"].split(", ")
                birthday = row["Birthday"]
                if birthday:
                    day, month = map(int, birthday.split("/"))
                    birthday = Birthday(day, month)
                else:
                    birthday = None
                record = Record(name, phones, birthday)
                self.add_record(record)
