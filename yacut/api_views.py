from flask import jsonify

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URL_map


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    data = {'url': url_map.original}
    return jsonify(data), 200
