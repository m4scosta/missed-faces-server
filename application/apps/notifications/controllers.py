from flask import Blueprint, redirect
from flask.ext.login import login_required, current_user
from flask.globals import request
from flask.helpers import url_for
from flask.json import jsonify
from flask.templating import render_template

from application.apps.notifications.forms import NotificationForm
from application.apps.notifications.models import NotificationMethod

notifications_mod = Blueprint('notifications', __name__, url_prefix='/notificacoes')

@notifications_mod.route("/nova", methods=['GET', 'POST'])
@login_required
def new():
    form = NotificationForm(user=current_user.id)

    if request.method == "GET":
        return render_template("notifications/new.html", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            notification_method = NotificationMethod(user=current_user.id)
            form.populate_obj(notification_method)
            notification_method.save()
            return jsonify(status="success", next=url_for("notifications.list_notification_methods"))
        return jsonify(status="error", errors=form.errors)


@notifications_mod.route("/", methods=['GET'])
@login_required
def list_notification_methods():
    methods = NotificationMethod.objects(user=current_user.id)
    return render_template("notifications/list.html", notification_methods=methods)


@notifications_mod.route("/delete/<string:notification_id>", methods=["GET"])
def delete(notification_id):
    notification = NotificationMethod.objects.get_or_404(id=notification_id)
    notification.delete()
    return jsonify(status="success")
