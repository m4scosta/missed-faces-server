from flask.helpers import url_for
from mongoengine import fields

from application.apps.base.models import BaseDocument


class Detector(BaseDocument):
    description = fields.StringField(max_length=255)
    location = fields.GeoPointField(required=True, unique=True)

    def get_absolute_url(self):
        return url_for('detectors', kwargs={'detector_id': self.id})

    def __unicode__(self):
        return self.description

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'location']
    }
