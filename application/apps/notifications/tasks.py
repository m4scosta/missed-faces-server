from application import celery


class NotificationTask(celery.Task):

    def run(self, found_person):
        print found_person
