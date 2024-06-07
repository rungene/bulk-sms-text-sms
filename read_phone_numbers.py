#!/usr/bin/env python3
import csv


def read_kenyan_phone_numbers(filename="sample.csv", delimiter=","):
    """Reads phone numbers from a CSV file, replaces numbers
    starting with '+254' with '0',and returns a list of
    modified phone numbers.

    Args:
        filename (str, optional): The name of the CSV file to read.
        Defaults to "sample.csv".
        delimiter (str, optional): The delimiter used in the CSV
        file. Defaults to "," (comma).

    Returns:
        list: A list of modified phone numbers (strings).
    """

    kenyan_phone_numbers = []
    try:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # Skip header - first row contains column names
                    line_count += 1
                    continue

                phone = row[35].strip()
                phone_number = phone.replace(' ', '')
                if phone_number.startswith('0') or \
                        phone_number.startswith('+254') or \
                        phone_number.startswith('254'):
                    if phone_number.startswith('+254'):
                        phone_number = '0' + phone_number[4:]
                    elif phone_number.startswith('254'):
                        phone_number = '0' + phone_number[3:]
                    kenyan_phone_numbers.append(phone_number)
                line_count += 1
                if line_count == 2:
                    break

    except FileNotFoundError:
        print(f'Error: file "{filename}" not found')
    except Exception as e:
        print(f'Error: {e}')
    if kenyan_phone_numbers:
        return kenyan_phone_numbers


if __name__ == "__main__":
    modified_numbers = read_kenyan_phone_numbers(filename="contacts.csv")
    print(modified_numbers)
