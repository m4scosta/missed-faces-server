import base64
import StringIO

from datetime import datetime
from PIL import Image

from flask import Blueprint
from flask import jsonify
from flask import request

from application.apps.detections.models import Detection
from application.apps.notifications.tasks import NotificationTask
from application.apps.recognition.task import RecognitionTask

detection_mod = Blueprint('detection', __name__, url_prefix='/detection')

def load_pil_image(face):
    size = (face['width'], face['height'])
    decoded_bytes = base64.b64decode(face['face'])
    return Image.frombytes("RGB", size, decoded_bytes)

def load_io_image(face):
    output = StringIO.StringIO()
    image = load_pil_image(face)

    image.save(output, format="JPEG")

    return output

@detection_mod.route("", methods=['POST'])
def create_detection():
    detection_data = request.get_json()

    faces = [load_io_image(face) for face in detection_data['faces']]
    detection = Detection(time=datetime.fromtimestamp(detection_data['time'] / 1e3), face=faces[0])
    # detection.save()

    RecognitionTask().apply_async((detection, ), link=NotificationTask().s())

    return jsonify(detection=detection)


@detection_mod.route("/list", methods=['GET'])
def list_detection():
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
