from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import check_short_id
from .views import BASE_URL, get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    data = {'url': url_map.original}
    return jsonify(data), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    custom_id = data.get('custom_id', '')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if custom_id in ['', None]:
        custom_id = get_unique_short_id()
    if URL_map.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            f'Имя "{custom_id}" уже занято.')
    if not check_short_id(custom_id) and custom_id not in ['', None]:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')
    new_url = URL_map(original=data['url'], short=custom_id)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(dict(
        url=new_url.original,
        short_link=f'{BASE_URL}{new_url.short}')
    ), HTTPStatus.CREATED
