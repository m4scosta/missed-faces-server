import cv2


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RecognitionService(object):
    __metaclass__ = Singleton

    @classmethod
    def get_instance(cls):
        return cls()

    def __init__(self):
        self.recognizer = cv2.createEigenFaceRecognizer(threshold=6000)

    def train(self, images, labels):
        self.recognizer.train(images, labels)

    def recognize(self, image):
        return self.recognizer.predict(image)

    def update_training(self, images, labels):
        self.recognizer.update(images, labels)
        print "recognizer updated"
