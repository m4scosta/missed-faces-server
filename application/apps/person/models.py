from mongoengine import fields
from flask.helpers import url_for
from mongoengine.document import EmbeddedDocument
from application.apps.auth.models import User

from application.apps.base.models import BaseDocument


class MissedPersonImage(EmbeddedDocument):
    image = fields.ImageField(size=(100, 100), required=True)


class MissedPerson(BaseDocument):
    user = fields.ReferenceField(User, required=True)
    name = fields.StringField(max_length=255, required=True)
    born_date = fields.DateTimeField()
    missed_date = fields.DateTimeField(required=True)
    images = fields.EmbeddedDocumentListField(MissedPersonImage)
    counter = fields.SequenceField()

    def get_absolute_url(self):
        return url_for('person', kwargs={'person_id': self.id})

    def __unicode__(self):
        return self.name

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'name'],
    }
