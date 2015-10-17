from flask.templating import render_template_string
import requests
import sendgrid

from mongoengine import fields

from application import app
from application.apps.auth.models import User
from application.apps.base.models import BaseDocument
from application import sg

__author__ = 'marcos'


class Notifier(object):

    def __init__(self, target):
        self.target = target

    def notify(self, target):
        raise NotImplementedError()


class EmailNotifier(Notifier):

    def notify(self, detection):
        print("sending email notification")
        message = sendgrid.Mail(subject="Pessoa encontrada",
                                recipients=[self.target],
                                from_email=app.config["DEFAULT_MAIL_SENDER"],
                                html=self.build_message_body(detection),
                                body=self.build_message_body(detection))

        print sg.send(message)
        print "email sent to {}".format(self.target)

    @staticmethod
    def build_message_body(detection):
        return render_template_string("email/person_found.html",
                                      detection=detection)


class URLPostNotifier(Notifier):

    def notify(self, detection):
        print("sending URL post notification")
        response = requests.post(self.target, data={"name": detection.person.name})

        if response.status_code != 200:
            print("Post notification of detection %s, to URL %s failed" %(detection.id, self.target))


class NotificationMethod(BaseDocument):
    user = fields.ReferenceField(User, required=True)
    notification_type = fields.StringField(regex="^email|post$", required=True)
    target = fields.StringField(required=True)

    meta = {
        'ordering': ['notification_type', 'created_at']
    }

    def get_notifier(self):
        if self.notification_type == "email":
            return EmailNotifier(target=self.target)
        elif self.notification_type == "post":
            return URLPostNotifier(target=self.target)
        return Notifier(target=self.target)
