from mongoengine import fields
from flask.helpers import url_for
from application.apps.base.models import BaseDocument


class MissedPerson(BaseDocument):
    name = fields.StringField(max_length=255, required=True)
    born_date = fields.DateTimeField()
    missed_at = fields.DateTimeField(required=True)

    def get_absolute_url(self):
        return url_for('person', kwargs={'person_id': self.id})

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'name'],
    }
