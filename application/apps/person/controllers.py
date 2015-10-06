from flask import Blueprint, redirect
from flask import jsonify
from flask import request
from flask.templating import render_template

from application.apps.person.forms import MissedPersonForm
from application.apps.person.models import MissedPersonImage
from application.apps.recognition.task import TrainingTask
from .models import MissedPerson

person_mod = Blueprint('person', __name__, url_prefix='/person')


@person_mod.route("/", methods=['GET'])
def person_form():
    form = MissedPersonForm(csrf_enabled=False)
    return render_template("person/create.html", form=form)


@person_mod.route("/", methods=['POST'])
def create_person():
    form = MissedPersonForm(csrf_enabled=False)

    if form.validate_on_submit():
        files = request.files.getlist('images')
        person = MissedPerson(**form.data)
        person.images = [MissedPersonImage(image=img) for img in files]

        person.save()

        TrainingTask().apply_async((person, ))

        return redirect('/person/')

    return render_template("person/create.html", form=form)


@person_mod.route("/list/", methods=['GET'])
def list_person():
    return jsonify(persons=MissedPerson.objects.all())


@person_mod.route("/<string:person_id>/", methods=['GET'])
def get_person(person_id):
    return jsonify(person=MissedPerson.objects.get_or_404(id=person_id))


@person_mod.route("/<string:person_id>/", methods=['DELETE'])
def delete_person(person_id):
    person = MissedPerson.objects.get_or_404(id=person_id)
    person.delete()

    del person.id

    return jsonify(person=person)
