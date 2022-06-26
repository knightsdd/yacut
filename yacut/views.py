import os
from random import randint

from flask import render_template, flash

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
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id == '':
            custom_id = get_unique_short_id()
        else:
            if URL_map.query.filter_by(short=custom_id).first() is not None:
                flash('Такая короткая ссылка уже занята!')
                return render_template('urlsform.html', form=form)
        
        new_url = URL_map(
            original=original_link,
            short=custom_id)
        db.session.add(new_url)
        db.session.commit()
        base_url = os.getenv('BASE_URL')
        full_short_url = f'{base_url}{custom_id}'
        return render_template(
            'urlsform.html',
            form=form,
            short_url=full_short_url)
    return render_template('urlsform.html', form=form)


if __name__ == '__main__':
    print(get_unique_short_id())
