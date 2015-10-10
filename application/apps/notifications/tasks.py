from application import celery
from application.apps.notifications.models import NotificationMethod


class NotificationTask(celery.Task):

    def run(self, detection):
        if detection is None:
            return None

        self.detection = detection
        methods = NotificationMethod.objects(user=detection.person.user)

        for method in methods:
            self.notify(method)

    def notify(self, method):
        notifier = method.get_notifier()
        notifier.notify(self.detection)
