import sys
import time

import cv2
import imutils
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imutils.video import VideoStream

import design

duration = 1000  # millisecond
freq = 440  # Hz

prototxt = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
NotHidden = {"person", "cat", "dog"}
net = cv2.dnn.readNetFromCaffe(prototxt, model)
global circles
circles = []
global isPressMarkUpButton
isPressMarkUpButton = False
global isPolyCreated
isPolyCreated = False


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


class UI(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.start_video()
        self.pushButton_n1.clicked.connect(self.mark_up)

    def mark_up(self):
        global isPressMarkUpButton
        if not isPressMarkUpButton:
            isPressMarkUpButton = True
        elif isPressMarkUpButton:
            isPressMarkUpButton = False

    def start_video(self):
        self.v1 = Video(src=0)
        # self.v2 = Video(src=0)
        # self.v3 = Video(src=0)
        print("test1")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(5)

    def update_video(self):
        print("test2S")
        # c = self.v1.get_polygon_frame()
        # cv2.imshow("main", c)
        c = self.v1.get_image_qt(self.v1.get_polygon_frame())
        self.video_1.setPixmap(c)
        self.video_2.setPixmap(c)
        self.video_3.setPixmap(c)
        self.video_4.setPixmap(c)



class Video:
    def __init__(self, src=0, color=(0, 255, 0), color2=(0, 0, 255), color3=(255, 0, 0), confidence=0.4):
        self.isPeopleRecg = True
        self.isAlarmEnabled = True

        self.vs = VideoStream(src=src).start()
        self.vc = cv2.VideoCapture(0)
        print("start")
        time.sleep(2.0)
        self.color = color
        self.color2 = color2
        self.color3 = color3
        self.isPlay = True
        self.frame = self.get_frame()
        self.confidence = confidence

    def get_frame(self, width=500):
        frame = self.vs.read()
        if frame is None:
            _, frame = self.vc.read()
        frame = imutils.resize(frame, width=width)

        return frame

    # For first cam-capture
    def detect_green_gumanoids(self):
        frame = self.get_frame()
        if not self.isPeopleRecg:
            return frame
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        print("detection")
        for i in np.arange(0, detections.shape[2]):
            if detections[0, 0, i, 2] < 0.3:
                continue
            if CLASSES[int(detections[0, 0, i, 1])] != "person":
                continue
            print("detected")
            label = "Gumanoid"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), self.color, 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 2)
        return frame

    def get_polygon_image(self):
        global circles
        global isPressMarkUpButton
        global isPolyCreated
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

        if not self.isPeopleRecg:
            return frame
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        print(detections)
        print("detection")
        for i in np.arange(0, detections.shape[2]):
            if detections[0, 0, i, 2] < 0.3:
                continue
            if CLASSES[int(detections[0, 0, i, 1])] != "person":
                continue
            print("detected")
            label = "Humanoid"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if (isPolyCreated == True):
                points = np.array(circles)
                if (inPolygon((startX + endX) / 2, (startY + endY) / 2, points[:, 0], points[:, 1])):
                    # if(isPixsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color3, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, "not a good guy", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color3, 2)
                # winsound.Beep(freq, duration)
                else:
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 2)
        return frame

    def get_image_qt(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        p = convertToQtFormat.scaled(300, 200, Qt.KeepAspectRatio)  # текущие координаты
        return QPixmap.fromImage(p)

    def play(self):
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
            self.isPeopleRecg = state


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = UI()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()
