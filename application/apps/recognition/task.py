from application import celery
from application.apps.recognition.service import RecognitionService


class RecognitionTask(celery.Task):

    recognition_service = RecognitionService()

    def run(self):
        print self.recognition_service, "OK"
