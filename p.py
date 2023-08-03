import datetime

upcoming_birthdays = []

def birthday_upcoming(birthdates, days):
    today = datetime.date.today()
    upcoming_date = today + datetime.timedelta(days=days)
    global upcoming_birthdays  # Access the global list of upcoming birthdays
    new_upcoming_birthdays = []
    for name, birthdate in birthdates.items():
        next_birthday = birthdate.replace(year=upcoming_date.year)
        if next_birthday < today:
            next_birthday = birthdate.replace(year=upcoming_date.year + 1)

        # Check if the next birthday falls within the range of upcoming dates
        while today <= next_birthday < upcoming_date:
            new_upcoming_birthdays.append((name, next_birthday))
            next_birthday = next_birthday.replace(year=next_birthday.year + 1)

    upcoming_birthdays += new_upcoming_birthdays  # Add new upcoming birthdays to the global list
    return new_upcoming_birthdays

birthdates = {
    'John': datetime.date(1990, 8, 31),
    'Alice': datetime.date(1985, 8, 2),
    'Bob': datetime.date(1995, 8, 31),
    'Charlie': datetime.date(1990, 1, 30),
    'Eve': datetime.date(1985, 2, 28),
    'Frank': datetime.date(1995, 3, 31),
    'Grace': datetime.date(1990, 9, 30),
    'Hank': datetime.date(1985, 5, 28),
    'Ivy': datetime.date(1995, 6, 28),
}

MAX_RETRIES = 100

def get_valid_integer_input(prompt):
    for _ in range(MAX_RETRIES):
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Введіть дійсне число.")
    raise ValueError("Забагато некоректних спроб введення числа.")


def main():
    try:
        while True:
            days_to_check = get_valid_integer_input("Скільки днів перевіряти (або введіть 0 для виходу)? ")

            if days_to_check <= 0:
                print("До побачення!")
                break

            upcoming_birthdays = birthday_upcoming(birthdates, days_to_check)

            if upcoming_birthdays:
                print(f"Дні народжень через {days_to_check} днів:")
                for name, birthdate in upcoming_birthdays:
                    print(f"{name}: {birthdate.strftime('%m-%d')}")
            else:
                print(f"Немає днів народжень впродовж {days_to_check} днів.")
    except ValueError as e:
        print(f"Помилка: {e}")


if __name__ == '__main__':
    main() 