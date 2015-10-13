import numpy as np
from scipy.ndimage import gaussian_filter
import cv2

__author__ = 'marcos'



class PreProcessor(object):

    def __init__(self, image):
        self.image = image

    def __call__(self, *args, **kwargs):
        return self._process()

    def _process(self):
        raise NotImplementedError()


class GammaCorrectionPreProcessor(PreProcessor):

    def __init__(self, image, gamma=0.5):
        super(GammaCorrectionPreProcessor, self).__init__(image)
        self.gamma = gamma

    def _process(self):
        self.image = (self.image / 255.0)
        self.image = cv2.pow(self.image, self.gamma)
        return np.uint8(self.image * 255)


class DifferenceOfGaussians(PreProcessor):

    first_kernel = (1, 1)
    second_kernel = (5, 5)

    def _process(self):
        blur_1 = gaussian_filter(self.image, 0.25)
        blur_2 = gaussian_filter(self.image, 2.0)
        return cv2.subtract(blur_1, blur_2)


class ContrastEqualizationPreProcessor(PreProcessor):

    def _process(self):
        return cv2.equalizeHist(self.image)


class PreProcessingQueue(object):

    _pre_processors = (GammaCorrectionPreProcessor, DifferenceOfGaussians, ContrastEqualizationPreProcessor)

    def process(self, image):
        for pre_processor in self._pre_processors:
            image = pre_processor(image)()
        return image
