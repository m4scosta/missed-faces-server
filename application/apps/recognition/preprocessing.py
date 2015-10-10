import numpy as np
import cv2

__author__ = 'marcos'



class PreProcessor(object):

    def __init__(self, image):
        self.image = image

    def __call__(self, *args, **kwargs):
        return self._process()

    def _process(self):
        raise NotImplementedError()


class GammaAdjustPreProcessor(PreProcessor):

    def __init__(self, image, gamma=1.0):
        super(GammaAdjustPreProcessor, self).__init__(image)
        self.gamma = gamma

    def _process(self):
        inverse_gamma = 1.0 / self.gamma
        table = np.array([((i / 255.0) ** inverse_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(self.image, table)


class DifferenceOfGaussians(PreProcessor):

    first_kernel = (2, 2)
    second_kernel = (4, 4)

    def _process(self):
        blur_1 = cv2.blur(self.image, self.first_kernel)
        blur_2 = cv2.blur(self.image, self.second_kernel)

        return cv2.subtract(blur_1, blur_2)


class ContrastEqualizationPreProcessor(PreProcessor):

    def _process(self):
        return cv2.equalizeHist(self.image)


class PreProcessingQueue(object):

    _pre_processors = (GammaAdjustPreProcessor, DifferenceOfGaussians,
                       ContrastEqualizationPreProcessor)

    def process(self, image):
        for pre_processor in self._pre_processors:
            image = pre_processor(image)()
        return image
