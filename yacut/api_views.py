import os
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import check_short_id
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    data = {'url': url_map.original}
    return jsonify(data), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    custom_id = ''
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        custom_id = data['custom_id']
        if custom_id in ['', None]:
            custom_id = get_unique_short_id()
        elif not check_short_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        elif URL_map.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                f'Имя "{custom_id}" уже занято.')
    else:
        custom_id = get_unique_short_id()

    new_url = URL_map(original=data['url'], short=custom_id)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(dict(
        url=new_url.original,
        short_link=f'{os.getenv("BASE_URL")}{new_url.short}')
    ), 201
