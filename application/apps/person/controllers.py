from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect
from flask import send_file
from flask.ext.login import current_user, login_required
from flask.helpers import url_for
from flask.templating import render_template

from application.apps.person.forms import MissedPersonForm
from application.apps.person.models import MissedPersonImage
from application.apps.recognition.task import TrainingTask
from .models import MissedPerson

person_mod = Blueprint('person', __name__, url_prefix='/desaparecidos')


@person_mod.route("/", methods=['GET'])
@login_required
def index():
    persons = MissedPerson.objects(user=current_user.id)
    return render_template("person/list.html", persons=persons)


@person_mod.route("/novo", methods=['GET', 'POST'])
@login_required
def new_person():
    form = MissedPersonForm()

    if request.method == "POST" and form.validate_on_submit():
        files = request.files.getlist('images')
        person = MissedPerson(user=current_user.id)
        form.populate_obj(person)
        person.images = [MissedPersonImage(image=img) for img in files]

        person.save()

        TrainingTask().apply_async((person, ))

        return redirect(url_for("person.list_person"))

    return render_template("person/create.html", form=form)


@person_mod.route("/list/", methods=['GET'])
@login_required
def list_person():
    return jsonify(persons=MissedPerson.objects(user=current_user.id))


@person_mod.route("/<string:person_id>/", methods=['GET'])
@login_required
def get_person(person_id):
    return jsonify(person=MissedPerson.objects.get_or_404(id=person_id))


@person_mod.route("/delete/<string:person_id>/", methods=['get'])
@login_required
def delete_person(person_id):
    person = MissedPerson.objects.get_or_404(id=person_id)
    person.delete()

    del person.id

    return jsonify(status="success")


@person_mod.route("/image/<string:person_id>/<int:index>/", methods=['GET'])
@login_required
def download_image(person_id, index):
    person = MissedPerson.objects.get_or_404(id=person_id)
    image = person.images[index]
    return send_file(image.image)
