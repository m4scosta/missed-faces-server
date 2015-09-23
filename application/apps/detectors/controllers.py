from flask import Blueprint
from flask import jsonify
from flask import request

from application.apps.detectors.models import Detector

detector_mod = Blueprint('detector', __name__, url_prefix='/detector')


@detector_mod.route("", methods=['POST'])
def create_detector():
    detector_data = request.get_json()
    detector = Detector(**detector_data)
    detector.save()
    return jsonify(detector=detector)


@detector_mod.route("/list", methods=['GET'])
def list_detector():
    return jsonify(detectors=Detector.objects.all())


@detector_mod.route("/<string:detector_id>", methods=['GET'])
def get_detector(detector_id):
    p = Detector.objects.get_or_404(id=detector_id).delete()
    return jsonify(detector=p)


@detector_mod.route("/<string:detector_id>", methods=['DELETE'])
def delete_detector(detector_id):
    detector = Detector.objects.get_or_404(id=detector_id)
    detector.delete()

    del detector.id

    return jsonify(detector=detector)
