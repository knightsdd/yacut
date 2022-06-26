from random import randint

from flask import render_template

from . import app, db
from .forms import UrlMapForm
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


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    # if form.validate_on_submit():

    return render_template('urlsform.html', form=form)


if __name__ == '__main__':
    print(get_unique_short_id())
