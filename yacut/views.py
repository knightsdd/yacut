from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import UrlMapForm
from .models import URL_map
from .utils import get_unique_short_id

BASE_URL = 'http://localhost/'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if form.custom_id.data is None:
            custom_id = get_unique_short_id()
        elif custom_id == '':
            custom_id = get_unique_short_id()
        else:
            if URL_map.query.filter_by(short=custom_id).first() is not None:
                flash(f'Имя {custom_id} уже занято!')
                return render_template('urlsform.html', form=form)

        new_url = URL_map(
            original=original_link,
            short=custom_id)
        db.session.add(new_url)
        db.session.commit()
        full_short_url = f'{BASE_URL}{custom_id}'
        return render_template(
            'urlsform.html',
            form=form,
            short_url=full_short_url)
    return render_template('urlsform.html', form=form)


@app.route('/<string:short>')
def redirect_by_short_url(short):
    url = URL_map.query.filter_by(short=short).first()
    if url is None:
        abort(404)
    return redirect(url.original)


if __name__ == '__main__':
    print(get_unique_short_id())
