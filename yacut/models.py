from datetime import datetime as dt

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def to_dict(self):
        pass

    def from_dict(self):
        pass
