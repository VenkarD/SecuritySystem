import sys
import time

import cv2
import imutils
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from imutils.video import VideoStream

import tensorflow as tf

import design

duration = 1000  # millisecond
freq = 440  # Hz

"""prototxt = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
NotHidden = {"person", "cat", "dog"}
net = cv2.dnn.readNetFromCaffe(prototxt, model)"""
global circles
circles = []
global isPressMarkUpButton
isPressMarkUpButton = False
global isPolyCreated
isPolyCreated = False

CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если 
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    16,     # cat
    17      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   #        номер класса = номер строки, нумерация с 1

def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))


def inPolygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c
    return c


def isPixsInArea(StartX, StartY, EndX, EndY, xp, yp):
    ret = False
    for y in range(StartY, EndY):
        for x in range(StartX, EndX):
            if inPolygon(x, y, xp, yp):
                ret = True
    return ret


#####begin#####
class DetectorAPI:
    def __init__(self, path_to_ckpt, path_to_labels):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        with open(path_to_labels) as f:
            self.labels = f.readlines()
        self.labels = [s.strip() for s in self.labels]

    def process(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0, i, 0] * im_height),
                        int(boxes[0, i, 1] * im_width),
                        int(boxes[0, i, 2] * im_height),
                        int(boxes[0, i, 3] * im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()
#####end#####


class UI(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None

        model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'  # HERE - название папки с моделью
        model_path = '../cocozoo/' + model_name + '/frozen_inference_graph.pb'  # HERE
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        self.detector = DetectorAPI(path_to_ckpt=model_path,
                                    path_to_labels=labels_path)

        self.start_video()
        self.pushButton_n1.clicked.connect(self.mark_up)

    def mark_up(self):
        global isPressMarkUpButton
        if not isPressMarkUpButton:
            isPressMarkUpButton = True
        elif isPressMarkUpButton:
            isPressMarkUpButton = False

    def start_video(self):
        # self.v1 = Video(src=0)
        # self.v2 = Video(src=0)
        # self.v3 = Video(src=0)
        self.v1 = Video(0, self.detector)  # HERE - первый аргумент - видеопоток
        print("test1")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(5)

    def update_video(self):
        print("test2S")
        # c = self.v1.get_polygon_frame()
        # cv2.imshow("main", c)
        # c = self.v1.get_image_qt(self.v1.get_polygon_frame())

        # c = self.v1.get_image_qt(self.v1.get_polygon_frame())
        c = self.v1.get_image_qt(self.v1.get_polygon_frame())

        self.video_1.setPixmap(c)
        self.video_2.setPixmap(c)
        self.video_3.setPixmap(c)
        self.video_4.setPixmap(c)


class Video:
    def __init__(self, src, detector,
                 color1=(0, 255, 0),
                 color2=(0, 0, 255),
                 color3=(255, 0, 0)):
        self.vc = cv2.VideoCapture(src)
        self.detector = detector
        print("start")
        time.sleep(2.0)
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.frame = self.get_frame()

    def get_frame(self, size=(640, 480)):
        _, frame = self.vc.read()
        frame = cv2.resize(frame, (640, 480))
        return frame

    # For first cam-capture
    def detect(self, img=None):  # бывш. detect_green_gumanoids
        if img is None:
            img = self.get_frame()
        boxes, scores, classes, num = self.detector.process(img)

        d_boxes = []
        d_scores = []
        d_classes = []
        for i in range(len(boxes)):
            if classes[i] in CLASSES_TO_DETECT and scores[i] > CONFIDENCE_LEVEL:
                d_boxes.append(boxes[i])
                d_scores.append(scores[i])
                d_classes.append(classes[i])
        return d_boxes, d_scores, d_classes

    def get_frame_detected(self, img=None):
        if img is None:
            img = self.get_frame()
        boxes, scores, classes = self.detect(img)
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),self.color1,2)
            y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
            cv2.putText(img, self.detector.labels[classes[i] - 1], (box[1], y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)

    def get_polygon_image(self, img=None):
        global circles
        global isPressMarkUpButton
        global isPolyCreated
        if img is None:
            img = self.get_frame()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.namedWindow("Frame")
        points = np.array(circles)

        if isPressMarkUpButton:
            cv2.setMouseCallback("Frame", mouse_drawing)
            for center_position in circles:
                cv2.circle(img, center_position, 2, (0, 0, 255), -1)

        if len(points) >= 4 and isPressMarkUpButton == False:
            cv2.polylines(img, np.int32([points]), 1, (255, 255, 255))
            isPolyCreated = True
            stencil = np.zeros(img.shape).astype(img.dtype)
            stencil[:] = (255, 255, 255)
            cv2.fillPoly(stencil, np.int32([points]), (255, 255, 255))
            img = cv2.bitwise_and(img, stencil)

        cv2.imshow("Frame", img)

        key = cv2.waitKey(1)
        if key == ord("d"):
            circles = []
            isPressMarkUpButton = False
            isPolyCreated = False
            img = self.get_frame()

        return img

    def get_polygon_frame(self):
        frame = self.get_polygon_image()

        boxes, scores, classes = self.detect(frame)

        for i in range(len(boxes)):
            # box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])  # было где-то тут
            box = boxes[i]
            (startX, startY, endX, endY) = box
            label = self.detector.labels[classes[i] - 1]

            if (isPolyCreated == True):
                points = np.array(circles)
                if (inPolygon((startX + endX) / 2, (startY + endY) / 2, points[:, 0], points[:, 1])):
                    # if(isPixsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color3, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, "not a good guy", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color3, 2)
                # winsound.Beep(freq, duration)
                else:
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color1, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    def get_image_qt(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        p = convertToQtFormat.scaled(300, 200, Qt.KeepAspectRatio)  # текущие координаты
        return QPixmap.fromImage(p)

    """def play(self):
        self.isPlay = True
        self.vs.play()

    def stop(self):
        self.isPlay = False
        self.vs.stop()

    def is_alarm(self, state=None):
        if state is None:
            return self.isAlarmEnabled
        else:
            self.isAlarmEnabled = state

    def is_recognition(self, state=None):
        if state is None:
            return self.isPeopleRecg
        else:
            self.isPeopleRecg = state"""


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = UI()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем прило
    # HERE !!! освободить ресурсы - DetectorAPI.close()

if __name__ == '__main__':
    main()
