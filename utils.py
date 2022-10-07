import random


def generate_random_string(digit=16):
    letters = 'abcedfghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    special_character = '#$%_-.+='
    string = random.sample(letters + numbers + special_character, digit)
    return ''.join(string)


def is_startswith_in_list(row, _list):
    for item in _list:
        if row.startswith(item):
            return False
    return True


def get_window_y_size(num):
    number = (int(num) + 1) * 35 + 3
    if number >= 563:
        number = 563
    return number