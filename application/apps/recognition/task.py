import numpy as np

from application import celery
from application.apps.person.models import MissedPerson
from application.apps.recognition.preprocessing import PreProcessingQueue
from .service import RecognitionService
from .util import read_image_as_np_array


class BaseTask(celery.Task):
    recognition_service = RecognitionService()

    def convert_image_to_np(self, detection):
        image = read_image_as_np_array(detection.face)
        pre_processed = self.pre_process(image)
        return pre_processed

    @staticmethod
    def pre_process(image):
        return PreProcessingQueue().process(image)


class RecognitionTask(BaseTask):

    def run(self, detection):
        person = self.call_recognizer(detection)

        if person is not None:
            detection.person = person
            detection.save()
            return detection

        return None

    def call_recognizer(self, detection):
        image = self.convert_image_to_np(detection)
        label, confidence = self.recognition_service.recognize(image)

        if label < 0:
            return None

        return MissedPerson.objects.get(counter=label)


class TrainingTask(BaseTask):

    def run(self, missed_person):
        self.train_recognizer(missed_person)
        return missed_person

    def train_recognizer(self, missed_person):
        raw_images = map(read_image_as_np_array, missed_person.images)
        images = np.asarray([self.pre_process(img) for img in raw_images])
        labels = np.asarray([missed_person.counter] * len(missed_person.images))

        self.recognition_service.update_training(images, labels)
