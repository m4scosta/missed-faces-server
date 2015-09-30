from flask.ext.wtf.form import Form
from wtforms import fields
from wtforms import validators


class MissedPersonForm(Form):
    name = fields.StringField(
        validators=[validators.Length(min=1, max=255), validators.DataRequired()]
    )
    missed_date = fields.DateField(
        validators=[validators.DataRequired()]
    )
    born_date = fields.DateField()
