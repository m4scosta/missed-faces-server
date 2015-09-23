from flask import Flask
from flask import render_template

from flask.ext.mongoengine import MongoEngine

from flask import g

from application.apps.recognition.service import RecognitionService
from .assets import register_assets
from .blueprints import register_blueprints


class Application(Flask):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.config.from_object('config')

    def get_recognizer(self):
        recognizer = getattr(g, '_recognizer', None)

        if recognizer is None:
            recognizer = g._recognizer = RecognitionService()

        return recognizer

# instantiate application
app = Application(__name__)

# create database
db = MongoEngine(app)


register_assets(app)
register_blueprints(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.route("/")
def index():
    return render_template("index.html")
