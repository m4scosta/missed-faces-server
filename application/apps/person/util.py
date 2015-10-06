__author__ = 'marcos'


def train_recognizer_with_registered_persons():
    from .models import MissedPerson
    from application.apps.recognition.task import RecognitionService
    from application.apps.recognition.util import person_image_list_to_np_array

    labels_and_images = MissedPerson.objects.values_list('counter', 'images')
    labels, images = person_image_list_to_np_array(labels_and_images)

    RecognitionService.get_instance().train(images, labels)
