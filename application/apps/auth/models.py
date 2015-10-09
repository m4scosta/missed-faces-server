from flask.ext.login import UserMixin
from application import login_manager
from application.apps.base.models import BaseDocument
from mongoengine import fields

__author__ = 'marcos'


class User(BaseDocument, UserMixin):
    email = fields.EmailField(required=True)
    password = fields.StringField(required=True)


@login_manager.user_loader
def provide_user(user_id):
    return User.objects.get(id=user_id)
