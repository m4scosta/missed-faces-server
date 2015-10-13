import sendgrid

__author__ = 'marcos'


class SendGridMail(sendgrid.SendGridClient):

    def __init__(self, app):
        super(SendGridMail, self).__init__(username_or_apikey=app.config['SENDGRID_API_KEY'])
