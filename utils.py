import random


def generate_random_string(digit=16):
    letters = 'abcedfghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    special_character = '#$%_-.+='
    string = random.sample(letters + numbers + special_character, digit)
    return ''.join(string)


def is_startswith_in_list(row, blacklist):
    for item in blacklist:
        if row.startswith(item):
            return True
    return False


def get_window_y_size(num):
    number = (int(num) + 1) * 35 + 3
    if number >= 563:
        number = 563
    return number


def is_text_valid(stage_type, text):
    match stage_type:
        case 'PANIC':
            if not (text.isnumeric() and int(text) > 0):
                return False
        case 'TANK':
            if not (text.isnumeric() and int(text) > 0):
                return False
        case 'DELAY':
            if not (text.isnumeric() and int(text) > 0):
                return False
        case 'SCRIPTED':
            if text == '':
                return False
        case 'SETUP':
            if not (text.isnumeric() and int(text) > 0):
                return False
        case 'ESCAPE':
            if text != '':
                return False
        case 'RESULTS':
            if text != '':
                return False
        case 'NONE':
            if text != '':
                return False
    return True


def standardized_scripted(text):
    text = text.replace('\"', '')
    if '.' in text:
        text = text.split('.')[0]
    return '\"' + text + '\"'


def string_to_list(old_string):
    new_list = []
    for row in old_string.split('\n'):
        if row != '':
            new_list.append(row)
    return new_list