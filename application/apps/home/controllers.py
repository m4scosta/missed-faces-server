from flask import Blueprint
from flask.ext.login import login_required, current_user
from flask.templating import render_template
from application.apps.detections.models import Detection
from application.apps.notifications.models import NotificationMethod
from application.apps.person.models import MissedPerson

home_mod = Blueprint('home', __name__)


@home_mod.route("/", methods=['GET'])
@login_required
def index():
    person_count = MissedPerson.objects(user=current_user.id).count()
    notification_count = NotificationMethod.objects(user=current_user.id).count()

    not_seen = Detection.objects(user=current_user.id, seen=False).count()
    return render_template("index.html",
                           person_count=person_count,
                           notification_count=notification_count,
                           not_seen=not_seen)
