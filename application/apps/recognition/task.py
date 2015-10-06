import numpy as np
from PIL import Image
from application import celery
from application.apps.recognition.service import RecognitionService
import tempfile


def create_temp_file(data):
    f = tempfile.TemporaryFile()
    f.write(data)
    return f


def read_image_as_np_array(missed_person_image):
    temp_file = create_temp_file(missed_person_image.image.read())
    pil_image = Image.open(temp_file)
    img = pil_image.convert("L")
    return np.asarray(img)


class BaseTask(celery.Task):
    recognition_service = RecognitionService()


class RecognitionTask(BaseTask):

    def run(self, detection):
        return self.call_recognizer(detection)

    def call_recognizer(self, detection):
        return str(detection)


class TrainingTask(BaseTask):

    def run(self, missed_person):
        print(missed_person)
        self.train_recognizer(missed_person)

    def train_recognizer(self, missed_person):
        print(missed_person.images)
        images = np.asarray(map(read_image_as_np_array, missed_person.images))
        labels = np.asarray([missed_person.counter] * len(missed_person.images))

        self.recognition_service.update_training(images, labels)
