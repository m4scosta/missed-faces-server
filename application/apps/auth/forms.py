# coding: utf-8
from flask.ext.wtf.form import Form
from mongoengine.errors import DoesNotExist
from wtforms import fields
from wtforms import validators
from wtforms.validators import ValidationError
from application.apps.auth.models import User

__author__ = 'marcos'


class SignInForm(Form):
    email = fields.StringField(validators=[validators.Email(), validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])
    password_2 = fields.PasswordField(validators=[validators.DataRequired()])

    def validate_email(self, field):
        if User.objects(email=self.data['email']):
            raise ValidationError(u"Email já cadastrado.")

    def validate_password_2(self, field):
        if self.data["password"] != self.data["password_2"]:
            raise ValidationError(u"Confirmação de senha inválida.")


class LoginForm(Form):
    email = fields.StringField(validators=[validators.Email(), validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])

    def validate(self):
        validation = super(LoginForm, self).validate()

        try:
            user = User.objects.get(email=self.data['email'])
            if user and user.password != self.data['password']:
                self.errors['__all__'] = [u"Usuário ou senha inválidos"]
                validation = False
        except DoesNotExist:
            self.errors['__all__'] = [u"Usuário ou senha inválidos"]
            validation = False

        return validation
