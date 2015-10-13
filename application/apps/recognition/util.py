import numpy as np
import cv2
from application.apps.recognition.preprocessing import PreProcessingQueue

__author__ = 'marcos'


def create_temp_file(data):
    # TODO: excluir arquivo temporario
    file_name = "/tmp/%d" % hash(data)
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    return file_name


def read_image_as_np_array(image):
    data = image.read()
    temp_file = create_temp_file(data)
    img = cv2.imread(temp_file, cv2.IMREAD_GRAYSCALE)
    img = cv2.equalizeHist(img)
    return cv2.resize(img, (100, 100))


def person_image_list_to_np_array(labels_and_images):
    labels = []
    np_images = []

    for label, images in labels_and_images:
        for image in images:
            np_image = read_image_as_np_array(image.image)
            processed_image = PreProcessingQueue().process(np_image)

            labels.append(label)
            np_images.append(processed_image)

    return np.asarray(labels), np.asarray(np_images)
