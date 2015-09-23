import datetime
from application import db


class BaseDocument(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {
        'abstract': True
    }
