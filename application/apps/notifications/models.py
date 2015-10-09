from application.apps.auth.models import User
from application.apps.base.models import BaseDocument
from mongoengine import fields

__author__ = 'marcos'


class NotificationMethod(BaseDocument):
    user = fields.ReferenceField(User, required=True)
    notification_type = fields.StringField(regex="^email|post$", required=True)
    target = fields.StringField(required=True)

    meta = {
        'ordering': ['notification_type', 'created_at']
    }
