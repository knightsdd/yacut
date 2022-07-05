import re
from random import randint

from .models import URL_map


def get_short_id() -> str:
    rand_list = []
    for _ in range(6):
        i = randint(0, 2)
        if i == 0:
            rand_list.append(chr(randint(48, 57)))
        elif i == 1:
            rand_list.append(chr(randint(65, 90)))
        else:
            rand_list.append(chr(randint(97, 122)))

    return ''.join(rand_list)


def get_unique_short_id() -> str:
    items = URL_map.query.all()
    current_idents = [item.short for item in items]
    new_ident = get_short_id()
    while new_ident in current_idents:
        new_ident = get_short_id()
    return new_ident


def check_short_id(string):
    match = re.fullmatch(r'[a-zA-Z|\d]{1,16}', string)
    return (True if match else False)
