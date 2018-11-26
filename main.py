import sys
import time

import cv2
import imutils

import numpy as np
import tensorflow as tf
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imutils.video import VideoStream

import design
import cameramode

duration = 1000  # millisecond
freq = 440  # Hz

global circles
circles = []
global isPressMarkUpButton
isPressMarkUpButton = False
global isPolyCreated
isPolyCreated = False
global secState
secState = False

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    16,     # cat
    17      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))


def in_polygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c
    return c


def is_pixels_in_area(start_x, start_y, end_x, end_y, xp, yp):
    """ret = False
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if in_polygon(x, y, xp, yp):
                ret = True
    return ret"""
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if in_polygon(x, y, xp, yp):
                return True
    return False


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

        im_height, im_width, _ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0, i, 0] * im_height),
                             int(boxes[0, i, 1] * im_width),
                             int(boxes[0, i, 2] * im_height),
                             int(boxes[0, i, 3] * im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        # self.default_graph.close()  # AttributeError: '_GeneratorContextManager' object has no attribute 'close'


class UI(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 600
        self.width360 = 800
        model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'  # HERE - название папки с моделью
        model_path = model_name + '/frozen_inference_graph.pb'  # HERE
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        self.detector = DetectorAPI(path_to_ckpt=model_path,
                                    path_to_labels=labels_path)
        self.start_video()
        self.setWindowTitle('Security System')
        self.pushButton_1.clicked.connect(self.mark_up)
        self.pushButton_2.clicked.connect(self.mark_down)
        self.comboBox_1.currentTextChanged.connect(self.video_one_change_mode)
        self.comboBox_2.currentTextChanged.connect(
            self.video_two_change_mode)  # есть подозрения что можно передавать значения в функцию
        self.comboBox_3.currentTextChanged.connect(self.video_three_change_mode)

    def resizeEvent(self, event):
        super().__init__()
        self.width_standard = self.video_1.width()
        self.width360 = self.video_3.width()

    @staticmethod
    def mark_up():
        global isPressMarkUpButton
        isPressMarkUpButton = True
        print('Button clicked ', isPressMarkUpButton)

    @staticmethod
    def mark_down():
        global isPressMarkUpButton
        isPressMarkUpButton = False
        print('Button clicked ', isPressMarkUpButton)
        cv2.destroyAllWindows()

    def start_video(self):
        # WORK VERSION
        self.v1 = Video(src=0, detector=self.detector)
        self.v2 = Video(src=0, detector=self.detector)
        self.v2.stop()
        self.v3 = Video(src=0, detector=self.detector)
        self.v3.stop()
        # END OF WORK VERSION

        # DEBUG VERSION
        """self.v1 = Video(src='../cat.mp4',detector=self.detector)
        self.v2 = Video(src='../people.mp4',detector=self.detector)
        self.v2.stop()
        self.v3 = Video(src='../people.mp4',detector=self.detector)
        self.v3.stop()
        self.count = 0"""
        # END OF DEBUG VERSION

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(1)

    def update_video(self):
        # DEBUG VERSION
        """self.v1.get_frame()
        self.count += 1
        if self.count % 30 == 0:
            print('Frame', self.count)
        if self.count < 925:
            return"""
        # END OF DEBUG VERSION

        if self.v1.isPlay:
            a = self.v1.get_image_qt(self.v1.get_smart_frame(self.width_standard), self.width_standard)
            self.video_1.setPixmap(a)
        if self.v2.isPlay:
            a = self.v2.get_image_qt(self.v2.get_smart_frame(self.width_standard), self.width_standard)
            self.video_2.setPixmap(a)
        if self.v3.isPlay:
            a = self.v3.get_image_qt(self.v3.get_smart_frame(self.width360), self.width_standard)
            self.video_3.setPixmap(a)
        #if self.v4.isPlay:
            #self.v4.get_security_detected(self.width_standard)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Вы действительно хотите закрыть охранную систему",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.detector.close()
            event.accept()
        else:
            event.ignore()

    def video_one_change_mode(self, value):
        self.change_mod_by_mod(value, self.v1)

    def video_two_change_mode(self, value):
        self.change_mod_by_mod(value, self.v2)

    def video_three_change_mode(self, value):
        self.change_mod_by_mod(value, self.v3)

    @staticmethod
    def change_mod_by_mod(value, obj):
        if value == "Обычный режим":
            obj.mode = cameramode.ORIGINAL
            cv2.destroyAllWindows()
        elif value == "Распознавание людей":
            obj.mode = cameramode.DETECT_OBJECTS
            cv2.destroyAllWindows()
        elif value == "Распознавание движения":
            obj.mode = cameramode.DETECT_MOTION
            cv2.destroyAllWindows()
        elif value == "Распознавание границ":
            obj.mode = cameramode.DETECT_BORDERS
        else:
            print(value + " is not find")
        print(value)


class Video:
    def __init__(self, src=0, detector=None, color1=(0, 255, 0),
                 color2=(0, 0, 255), color3=(255, 0, 0), mode=cameramode.ORIGINAL):
        self.mode = mode
        self.mode1 = mode
        self.mode2 = mode
        self.mode3 = mode
        self.vc = cv2.VideoCapture(src)
        # DEBUG VERSION
        self.vs = VideoStream(src=src).start()
        # END OF DEBUG VERSION
        self.detector = detector
        print("start")
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.isPlay = True

    def get_smart_frame(self, width=500):
        # пока что не реализовано обнаружение движения - константа cameramode.DETECT_MOTION
        if self.mode == cameramode.DETECT_OBJECTS:
            return self.get_frame_detected(width)
        elif self.mode == cameramode.DETECT_BORDERS:
            return self.get_polygon_frame(width)
        else:
            return self.get_frame(width)

    def get_frame(self, width=500):
        # WORK VERSION
        frame = self.vs.read()
        if frame is None:
            _, frame = self.vc.read()
        # frame = imutils.resize(frame, width=width)
        # END OF WORK VERSION

        # DEBUG VERSION
        """_, frame = self.vc.read()"""
        # END OF DEBUG VERSION

        return frame

    # For first cam-capture
    def detect(self, width=500, img=None):
        if img is None:
            img = self.get_frame(width)
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

    def get_frame_detected(self, width=500, img=None):
        if img is None:
            img = self.get_frame(width)

        boxes, scores, classes = self.detect(width=width, img=img)
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), self.color1, 2)
            y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
            cv2.putText(img, self.detector.labels[classes[i] - 1], (box[1], y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return img

    def get_security_detected(self, width=500, img=None):
        global secState

        if img is None:
            img = self.get_frame(width)
            boxes, scores, classes = self.detect(width=width, img=img)

        if secState != (len(boxes) > 0):
            secState = (len(boxes) > 0)
        if secState:
            logger.debug("Security came")
        else:
            logger.debug("Security gone")

    def get_polygon_image(self, width=700, img=None):
        global circles
        global isPressMarkUpButton
        global isPolyCreated
        if img is None:
            img = self.get_frame(width)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # продублировано в get_image_qt()

        if isPressMarkUpButton:
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

        if isPressMarkUpButton:
           cv2.imshow("Frame", img)



        key = cv2.waitKey(1)
        if key == ord("d"):
            circles = []
            isPressMarkUpButton = False
            isPolyCreated = False
            img = self.get_frame()

        return img

    def get_polygon_frame(self, width=500):
        frame = self.get_polygon_image(width)
        # (w, h) = frame.shape[:2]

        boxes, scores, classes = self.detect(width=width, img=frame)
        print(len(boxes), 'object(s) detected')

        for i in range(len(boxes)):
            box = boxes[i]
            # box = box * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box
            label = self.detector.labels[classes[i] - 1]

            if isPolyCreated:
                # print('ok its draw')
                points = np.array(circles)
                if (in_polygon((box[1] + box[3]) / 2, (box[0] + box[3]) / 2, points[:, 0], points[:, 1])):
                    # print('draw 1')
                    # if(isPixelsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color3, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, "not a good guy", (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color3, 2)
                else:
                    # print('draw 2')
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color1, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, label, (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    @staticmethod
    def get_image_qt(frame, width=600):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(700, width, Qt.KeepAspectRatio)  # текущие координаты
        return QPixmap.fromImage(p)

    def play(self):
        self.isPlay = True
        self.vs.play()

    def stop(self):
        self.isPlay = False
        self.vs.stop()

    def set_mode(self, state=None):
        if state is None:
            return self.mode
        else:
            self.mode = state


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = UI()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()
