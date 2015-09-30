import cv2


class RecognitionService(object):

    def __init__(self):
        self.recognizer = cv2.createLBPHFaceRecognizer(threshold=10000)

    def train(self, images, labels):
        self.recognizer.train(images, labels)

    def recognize(self, image):
        return self.recognizer.predict(image)

    def update_training(self, images, labels):
        self.recognizer.update(images, labels)


# if __name__ == '__main__':
#     def read_csv():
#         imgs = []
#         lbls = []
#
#         w, h = 0, 0
#         with open('/home/marcos/faces/db.csv', 'rb') as db:
#             reader = csv.reader(db, delimiter=';')
#             for row in reader:
#                 img = cv2.equalizeHist(cv2.imread(row[0], cv2.IMREAD_GRAYSCALE))
#                 lbl = int(row[1])
#
#                 if w and h:
#                     img = cv2.resize(img, (w, h))
#                 else:
#                     w, h = img.shape
#
#                 imgs.append(img)
#                 lbls.append(lbl)
#         return imgs, lbls, (w, h)
#
#
#     names = {1: "MARCOS", 2: "UNKNOWN"}
#
#     images, labels, shape = read_csv()
#
#     # test_img = images.pop()
#     # test_label = labels.pop()
#
#     service = RecognitionService()
#     service.train(np.array(images), np.array(labels))
#
#     cap = cv2.VideoCapture(1)
#     cascade = cv2.CascadeClassifier("/home/marcos/projects/securityFaceRec/facerec/py/apps/videofacerec/haarcascade_frontalface_alt2.xml")
#
#     while True:
#         ret, frame = cap.read()
#
#         gray = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
#
#         # faces = cascade.detectMultiScale(gray, 1.1)
#
#         # if len(faces):
#         #     x, y, w, h = faces[0]
#         #
#         #     face = cv2.resize(gray[y:y+h, x:x+w], shape)
#         #
#         gray = cv2.resize(gray, shape)
#         predicted = service.recognize(gray)
#         # print "Predicted label = %d (confidence=%.2f)" % predicted
#
#         if predicted[0] >= 0:
#             cv2.putText(gray, names[predicted[0]], (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
#             # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
#
#         cv2.imshow('frame', gray)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
