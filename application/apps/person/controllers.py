from flask import Blueprint
from flask import jsonify
from flask import request

from .models import MissedPerson

person_mod = Blueprint('person', __name__, url_prefix='/person')


@person_mod.route("", methods=['POST'])
def create_person():
    person_data = request.get_json()
    person = MissedPerson(**person_data)
    person.save()
    return jsonify(person=person)


@person_mod.route("/list", methods=['GET'])
def list_person():
    return jsonify(persons=MissedPerson.objects.all())


@person_mod.route("/<string:person_id>", methods=['GET'])
def get_person(person_id):
    p = MissedPerson.objects.get_or_404(id=person_id).delete()
    return jsonify(person=p)


@person_mod.route("/<string:person_id>", methods=['DELETE'])
def delete_person(person_id):
    person = MissedPerson.objects.get_or_404(id=person_id)
    person.delete()

    del person.id

    return jsonify(person=person)
