from flask import Flask
from flask import render_template
from flask.ext.login import LoginManager

from flask.ext.mongoengine import MongoEngine

from application.email import SendGridMail
from .apps.recognition.service import RecognitionService
from .assets import register_assets
from .blueprints import register_blueprints
from .tasks import setup_celery
from .apps.person.util import train_recognizer_with_registered_persons



# instantiate application
app = Flask(__name__)
app.config.from_object('config')

# create database
db = MongoEngine(app)

# task queue setup
celery = setup_celery(app)

# mail
sg = SendGridMail(app)

# auth
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

register_assets(app)
register_blueprints(app)
train_recognizer_with_registered_persons()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.route("/")
def index():
    return render_template("index.html")
