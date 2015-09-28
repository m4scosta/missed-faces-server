from application import celery
from application.apps.recognition.service import RecognitionService


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
        pass
