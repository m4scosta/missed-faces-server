# coding: utf-8
from flask.ext.wtf.form import Form
from wtforms import fields
from wtforms import validators
from application.apps.notifications.models import NotificationMethod

__author__ = 'marcos'


class NotificationForm(Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NotificationForm, self).__init__(*args, **kwargs)

    notification_type = fields.SelectField(label="Tipo", choices=[("email", "E-mail"), ("post", "Post em URL")],
                                           validators=[validators.DataRequired()])
    target = fields.StringField(label="Destino", validators=[validators.DataRequired()])

    def validate_target(self, field):
        if self.data['notification_type'] == "email":
            validators.Email()(self, field)

        if self.data['notification_type'] == "post":
            validators.URL()(self, field)

    def validate(self):
        valid = super(NotificationForm, self).validate()

        filters = self.data
        filters['user'] = self.user

        if NotificationMethod.objects(**filters):
            self.errors['__all__'] = [u"Método de notificação já cadastrado."]
            valid = False

        return valid
