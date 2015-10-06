import cv2

import numpy as np

from application import celery
from application.apps.person.models import MissedPerson
from .service import RecognitionService
from .util import read_image_as_np_array


class BaseTask(celery.Task):
    recognition_service = RecognitionService()


class RecognitionTask(BaseTask):

    def run(self, detection):
        return self.call_recognizer(detection)

    def call_recognizer(self, detection):
        image = read_image_as_np_array(detection.face)
        label, confidence = self.recognition_service.recognize(image)

        if label < 0:
            return None

        return MissedPerson.objects.get(counter=label)


class TrainingTask(BaseTask):

    def run(self, missed_person):
        self.train_recognizer(missed_person)
        return missed_person

    def train_recognizer(self, missed_person):
        images = np.asarray(map(read_image_as_np_array, missed_person.images))
        labels = np.asarray([missed_person.counter] * len(missed_person.images))

        self.recognition_service.update_training(images, labels)
