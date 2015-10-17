import datetime

from flask.helpers import url_for
from mongoengine import fields

from application.apps.auth.models import User
from application.apps.base.models import BaseDocument
from application.apps.person.models import MissedPerson


class Detection(BaseDocument):
    user = fields.ReferenceField(User, required=True)
    received_at = fields.DateTimeField(default=datetime.datetime.now(), required=True)

    face = fields.ImageField(required=True)
    time = fields.DateTimeField(required=True)
    person = fields.ReferenceField(MissedPerson, required=True)

    latitude = fields.StringField(required=True)
    longitude = fields.StringField(required=True)

    seen = fields.BooleanField(default=False)

    def get_absolute_url(self):
        return url_for('detection', kwargs={'detection_id': self.id})

    def __unicode__(self):
        return "Detection {}".format(self.received_at)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
    }
