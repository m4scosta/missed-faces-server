from flask import Blueprint
from flask import jsonify
from flask import request

from application.apps.detections.models import Detection
from application.apps.real_time.tasks import NotificationTask
from application.apps.recognition.task import RecognitionTask

detection_mod = Blueprint('detection', __name__, url_prefix='/detection')


@detection_mod.route("", methods=['POST'])
def create_detection():
    detection_data = request.get_json()
    detection = Detection(**detection_data)
    detection.save()

    # RecognitionTask.delay(link=NotificationTask.s())

    return jsonify(detection=detection)


@detection_mod.route("/list", methods=['GET'])
def list_detection():
    RecognitionTask().apply_async((None, ), link=NotificationTask().s())
    return jsonify(detections=Detection.objects.all())


@detection_mod.route("/<string:detection_id>", methods=['GET'])
def get_detection(detection_id):
    p = Detection.objects.get_or_404(id=detection_id).delete()
    return jsonify(detection=p)


@detection_mod.route("/<string:detection_id>", methods=['DELETE'])
def delete_detection(detection_id):
    detection = Detection.objects.get_or_404(id=detection_id)
    detection.delete()

    del detection.id

    return jsonify(detection=detection)
