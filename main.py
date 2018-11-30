import logging
import sys
import time

import cv2
import imutils

import numpy as np
# import tensorflow as tf
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imutils.video import VideoStream
from datetime import datetime

#import design
import SecuritySystemGUI
import Settings

import cameramode
from frame_analysis.object_detector import ObjectDetector
from frame_analysis.border_detector import BorderDetector
from frame_analysis.motion_detector import MotionDetector

from datetime import datetime

duration = 1000  # millisecond
freq = 440  # Hz

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

CAM_FPS = 25  # позже получить программно для каждой камеры, пока что так
PROCESS_PERIOD = 5  # период обновления информации детекторами
CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    16,     # cat
    17      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1

# bad bad rly bad code
# will be reworked later
# don't read just scroll down
global security_curr_state
security_curr_state = False
global security_prev_state
security_prev_state = False
global security_check_series
security_check_series = 5  # количество кадров в серии, если вдруг с первого раза сеть его не распознала
global security_check_period
security_check_period = 30 * CAM_FPS - security_check_series  # период проверки охранника
global security_frame_counter
security_frame_counter = security_check_period - 1


def in_polygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c
    return c

# Иконка загрузки
class Splash(QSplashScreen):
    def __init__(self, *arg, **args):
        QSplashScreen.__init__(self, *arg, **args)
        self.setCursor(Qt.BusyCursor)
        self.setPixmap(QPixmap("boot.jpg"))
        loaut = QVBoxLayout(self)
        loaut.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))

# Окно Настроек
class SecWin(QWidget, Settings.Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Settings')
        self.returnButton.clicked.connect(self.returnToMain)

    def returnToMain(self, event):
        self.destroy()


class UI(QMainWindow, SecuritySystemGUI.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 1200
        self.width360 = 1600
        model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'  # HERE - название папки с моделью
        model_path = model_name + '/frozen_inference_graph.pb'  # HERE
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        self.object_detector = ObjectDetector(path_to_ckpt=model_path,
                                              path_to_labels=labels_path,
                                              classes_to_detect = CLASSES_TO_DETECT,
                                              confidence_level = CONFIDENCE_LEVEL)
        self.start_video()
        self.setWindowTitle('Security System')
        self.pushButton_1.clicked.connect(self.mark_up_1)
        self.pushButton_3.clicked.connect(self.mark_up_2)
        self.pushButton_5.clicked.connect(self.mark_up_3)
        self.pushButton_8.clicked.connect(self.setings_open)
        self.pushButton_9.clicked.connect(self.close)
        self.comboBox_1.currentTextChanged.connect(self.video_one_change_mode)
        self.comboBox_2.currentTextChanged.connect(self.video_two_change_mode)  # есть подозрения что можно передавать значения в функцию
        self.comboBox_3.currentTextChanged.connect(self.video_three_change_mode)
        self.secondWin = None
        self.update_video()

    def resizeEvent(self, event):
        # super().__init__()  # ?
        self.width_standard = self.comboBox_1.width()*5
        self.width360 = self.comboBox_2.width()*5

    def setings_open(self, event):
        print("it's realy settingsButton")
        if not self.secondWin:
            self.secondWin = SecWin()
        self.secondWin.show()



    #@staticmethod
    def mark_up_1(self, event):
        if not self.v1.border_detector.isPressMarkUpButton:
            # self.v1.border_detector.isPressMarkUpButton = True
            self.v1.border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_1.setText('Деактивировать')
        else:
            # self.v1.border_detector.isPressMarkUpButton = False
            self.v1.border_detector.end_selecting_region()
            self.pushButton_1.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.v1.border_detector.isPressMarkUpButton)

    def mark_up_2(self, event):
        if not self.v2.border_detector.isPressMarkUpButton:
            # self.v2.border_detector.isPressMarkUpButton = True
            self.v2.border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_3.setText('Деактивировать')
        else:
            # self.v2.border_detector.isPressMarkUpButton = False
            self.v2.border_detector.end_selecting_region()
            self.pushButton_3.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.v2.border_detector.isPressMarkUpButton)

    def mark_up_3(self, event):
        if not self.v3.border_detector.isPressMarkUpButton:
            # self.v3.border_detector.isPressMarkUpButton = True
            self.v3.border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_5.setText('Деактивировать')
        else:
            # self.v3.border_detector.isPressMarkUpButton = False
            self.v3.border_detector.end_selecting_region()
            self.pushButton_5.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.v3.border_detector.isPressMarkUpButton)

    @staticmethod
    def mark_down():
        self.v4.border_detector.isPressMarkUpButton = False
        print('Button clicked ', self.v4.border_detector.isPressMarkUpButton)
        cv2.destroyAllWindows()

    def start_video(self):
        vsrc1, vsrc2, vsrc3, vsrc4 = None, None, None, None
        videosource = 'cameras'
        if len(sys.argv) > 1:
            videosource = sys.argv[1]

        if (videosource == 'files'):
            vsrc1 = '../people.mp4'
            vsrc2 = '../people.mp4'
            vsrc3 = '../people.mp4'
            vsrc4 = '../people.mp4'
        else:
            vsrc1 = 'rtsp://192.168.1.203:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrc2 = 'rtsp://192.168.1.135:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrc3 = 'rtsp://192.168.1.163:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'

            vsrc4 = 0

        self.v1 = Video(src=vsrc1,
                        object_detector=self.object_detector,
                        border_detector=BorderDetector(),
                        motion_detector=MotionDetector(),
                        init_fc=0)
        self.v1.mode1 = self.v1.mode
        self.v2 = self.v1
        self.v3 = self.v1
        # self.v1.stop()
        # self.v2 = Video(src=vsrc2,
        #                 object_detector=self.object_detector,
        #                 border_detector=BorderDetector(),
        #                 motion_detector=MotionDetector(),
        #                 init_fc=1)
        # #self.v2 = self.v1
        # self.v2.mode2 = self.v2.mode
        # # self.v2.stop()
        # self.v3 = Video(src=vsrc3,
        #                 object_detector=self.object_detector,
        #                 border_detector=BorderDetector(),
        #                 motion_detector=MotionDetector(),
        #                 init_fc=2)
        # #self.v3 = self.v1
        self.v3.mode3 = self.v3.mode
        # # self.v3.stop()
        self.v4 = Video(src=vsrc4,
                        object_detector=self.object_detector,
                        border_detector=BorderDetector(),
                        motion_detector=MotionDetector(),
                        init_fc=3)
        # self.v4.stop()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(40)

    def update_video(self):
        if self.v1.isPlay:
            a = self.v1.get_image_qt(self.v1.get_smart_frame(self.width_standard), self.width_standard)
            self.video_1.setPixmap(a)
        if self.v2.isPlay:
            a = self.v2.get_image_qt(self.v2.get_smart_frame(self.width_standard), self.width_standard)
            self.video_2.setPixmap(a)
        if self.v3.isPlay:
            a = self.v3.get_image_qt(self.v3.get_smart_frame(self.width_standard), self.width_standard)
            self.video_3.setPixmap(a)
        if self.v4.isPlay:
            self.v4.get_security_detected(self.v4.get_frame(self.width_standard))


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Вы действительно хотите закрыть охранную систему",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.object_detector.close()
            self.v1.vc.release()
            self.v1.vs.stop()
            self.v2.vc.release()
            self.v2.vs.stop()
            self.v3.vc.release()
            self.v3.vs.stop()
            #self.v4.vc.release()
            #self.v4.vs.stop()
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
        if (obj.mode == cameramode.DETECT_MOTION):
            obj.motion_detector.clear_queue()

        if value == "Обычный режим":
            obj.mode = cameramode.ORIGINAL
            cv2.destroyAllWindows()
        elif value == "Распознавание людей":
            obj.mode = cameramode.DETECT_OBJECTS
            cv2.destroyAllWindows()
        elif value == "Распознавание движения":
            obj.motion_detector.clear_queue()
            obj.mode = cameramode.DETECT_MOTION
            cv2.destroyAllWindows()
        elif value == "Распознавание границ":
            obj.mode = cameramode.DETECT_BORDERS
        else:
            print(value + " is not find")
        print(value)


class Video:
    def __init__(self, src=0, object_detector=None, border_detector=None,
                 motion_detector=None, color1=(0, 255, 0), color2=(0, 0, 255),
                 color3=(255, 0, 0), mode=cameramode.ORIGINAL, init_fc = 0):
        self.mode = mode
        # для чего столько?
        self.mode1 = mode
        self.mode2 = mode
        self.mode3 = mode
        self.vc = cv2.VideoCapture(src)
        self.vs = VideoStream(src=src).start()
        self.object_detector = object_detector
        self.border_detector = border_detector
        self.motion_detector = motion_detector
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.last_gf_func = lambda frame: frame  # последний результат обработки (в виде функции)
        self.frame_counter = init_fc
        self.isPlay = True
        print("start")

    def get_smart_frame(self, width=500):
        frame = self.get_frame(width)

        # bad code
        if self.border_detector.isPressMarkUpButton:
            cv2.imshow(self.border_detector.windowId, self.border_detector.get_frame_polygon(frame))

        self.frame_counter = (self.frame_counter + 1) % PROCESS_PERIOD
        if self.mode == cameramode.ORIGINAL:
            return frame

        if self.frame_counter == 0:
            if self.mode == cameramode.DETECT_OBJECTS:
                boxes, scores, classes = self.object_detector.process(frame)
                self.last_gf_func = lambda frame:  \
                    self.get_frame_objects(frame, boxes, classes)
            elif self.mode == cameramode.DETECT_MOTION:
                boxes = self.motion_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.get_frame_motion(frame, boxes)
            elif self.mode == cameramode.DETECT_BORDERS:
                boxes, scores, classes = self.object_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.get_frame_borders(frame, boxes, classes)
            else:
                self.last_gf_func = lambda frame: frame
        return self.last_gf_func(frame)


    def get_frame(self, width=500):
        frame = self.vs.read()
        if frame is None:
            _, frame = self.vc.read()
        # frame = imutils.resize(frame, width=width)
        return frame

    def get_frame_objects(self, frame, boxes, classes):
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(frame, (box[3], box[2]), (box[1], box[0]), self.color1, 2)
            y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
            cv2.putText(frame, self.object_detector.labels[classes[i] - 1], (box[1], y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    def get_frame_motion(self, frame, boxes):
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), self.color1, 2)
        return frame

    def get_frame_borders(self, frame, boxes, classes):
        if not self.border_detector.isPolyCreated:
            return frame

        frame = self.border_detector.get_frame_polygon(frame)  # ?
        #print(len(boxes), 'object(s) detected')

        for i in range(len(boxes)):
            box = boxes[i]
            (startX, startY, endX, endY) = box
            label = self.object_detector.labels[classes[i] - 1]

            # TODO создать функцию, которая рисует рамки с подписями
            if self.border_detector.isPolyCreated:
                # print('ok its draw')
                points = np.array(self.border_detector.circles)
                if (in_polygon((box[1] + box[3]) / 2, (box[0] + box[2]) / 2, points[:, 0], points[:, 1])):
                    # print('draw 1')
                    # if(isPixelsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color2, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, "not a good guy", (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color2, 2)
                else:
                    # print('draw 2')
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color1, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, label, (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    def get_security_detected(self, frame):
        global security_curr_state
        global security_prev_state
        global security_check_series
        global security_check_period
        global security_frame_counter

        security_frame_counter = (security_frame_counter + 1) % security_check_period

        if security_frame_counter == 0:
            security_prev_state = security_curr_state
            security_curr_state = False
        if not security_curr_state and security_frame_counter < security_check_series:
            boxes, scores, classes = self.object_detector.process(frame)
            for oneclass in classes:
                if oneclass == 1:  # person
                    security_curr_state = True
                    break
        elif security_frame_counter == security_check_series and \
                security_curr_state != security_prev_state:
            print('{}: охранник {}'.format(datetime.now().\
                    strftime('%d.%m.%y %H:%M'),\
                    'на месте' if security_curr_state else 'отсутствует'))

        """if security_state != (len(boxes) > 0):
            security_state = (len(boxes) > 0)
        if security_state:
            logger.debug("Security came")
        else:
            logger.debug("Security gone")"""

    @staticmethod
    def get_image_qt(frame, width=600):
        assert frame is not None, 'Кадр пуст'
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(1400, width*0.5, Qt.KeepAspectRatio)  # текущие координаты
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

starttime = datetime.now()
global lasttime

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    splash = Splash()
    splash.show()
    window = UI()  # Создаём объект класса ExampleApp
    window.object_detector.process(np.zeros((1, 1, 3)))

    #window.setWindowOpacity(0.5)
    # pal = window.palette()
    # pal.setBrush(QPalette.Normal, QPalette.Background,
    #               QBrush(QPixmap("Fone.jpg")))
    # window.setPalette(pal)
    # window.setAutoFillBackground(True)
    window.setWindowIcon(QIcon("icon.png"))
    window.show()  # Показываем окно
    splash.finish(window)
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()