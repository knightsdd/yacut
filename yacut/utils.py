import random
import re
import string

from . import MAX_LENGTH_SHORT
from .models import URL_map


def get_short_id(max_length) -> str:
    rand_list = random.choices(string.ascii_letters + string.digits,
                               k=max_length)
    return ''.join(rand_list)


def get_unique_short_id() -> str:
    new_ident = get_short_id(MAX_LENGTH_SHORT)
    while URL_map.query.filter_by(short=new_ident).first() is not None:
        new_ident = get_short_id(MAX_LENGTH_SHORT)
    return new_ident


def check_short_id(string) -> bool:
    match = re.fullmatch(r'[a-zA-Z|\d]{1,16}', string)
    return (True if match else False)
