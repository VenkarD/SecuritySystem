import logging
import sys
import time

import cv2
import tensorflow as tf
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime

#import design
import SecuritySystemGUI
import cameramode
from videotool import VideoTool
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

CAMERAS_COUNT = 3
CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    16,     # cat
    17      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1


def get_image_qt(frame, width=600):
    assert frame is not None, 'Кадр пуст'
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
    p = convert_to_qt_format.scaled(1400, width*0.5, Qt.KeepAspectRatio)  # текущие координаты
    return QPixmap.fromImage(p)

# Иконка загрузки
class Splash(QSplashScreen):
    def __init__(self, *arg, **args):
        QSplashScreen.__init__(self, *arg, **args)
        self.setCursor(Qt.BusyCursor)
        self.setPixmap(QPixmap("boot.jpg"))
        loaut = QVBoxLayout(self)
        loaut.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.progress = QProgressBar(self)
        #self.progress.setValue(0)
        #self.progress.setMaximum(100)
        #loaut.addWidget(self.progress)
        #self.showMessage(u"Пример заставки", Qt.AlignTop)
        #self.startTimer(1000)
        #self.progress.setMaximum(0)
    #def timerEvent(self, event):
        #self.progress.setValue(self.progress.value() + 1)
        #event.accept()

class SecondWindow(QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        self.setWindowTitle('Settings')
        self.build()

    def build(self):
        self.mainLayout = QVBoxLayout()

        self.buttons = []
        for i in range(5):
            but = QPushButton('button {}'.format(i), self)
            self.mainLayout.addWidget(but)
            self.buttons.append(but)
        self.setLayout(self.mainLayout)

class UI(QMainWindow, SecuritySystemGUI.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 1200
        self.width360 = 1600

        self.video_labels = [self.video_1, self.video_2, self.video_3]

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
            self.secondWin = SecondWindow(self)
        self.secondWin.show()



    #@staticmethod
    def mark_up_1(self, event):
        if not self.videotools[0].border_detector.isPressMarkUpButton:
            # self.videotools[0].border_detector.isPressMarkUpButton = True
            self.videotools[0].border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_1.setText('Деактивировать')
        else:
            # self.videotools[0].border_detector.isPressMarkUpButton = False
            self.videotools[0].border_detector.end_selecting_region()
            self.pushButton_1.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.videotools[0].border_detector.isPressMarkUpButton)

    def mark_up_2(self, event):
        if not self.videotools[1].border_detector.isPressMarkUpButton:
            # self.videotools[1].border_detector.isPressMarkUpButton = True
            self.videotools[1].border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_3.setText('Деактивировать')
        else:
            # self.videotools[1].border_detector.isPressMarkUpButton = False
            self.videotools[1].border_detector.end_selecting_region()
            self.pushButton_3.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.videotools[1].border_detector.isPressMarkUpButton)

    def mark_up_3(self, event):
        if not self.videotools[2].border_detector.isPressMarkUpButton:
            # self.videotools[2].border_detector.isPressMarkUpButton = True
            self.videotools[2].border_detector.start_selecting_region(str(datetime.now()))
            self.pushButton_5.setText('Деактивировать')
        else:
            # self.videotools[2].border_detector.isPressMarkUpButton = False
            self.videotools[2].border_detector.end_selecting_region()
            self.pushButton_5.setText('Обозначить границы')
            # cv2.destroyAllWindows()
        print('Button clicked ', self.videotools[2].border_detector.isPressMarkUpButton)

    @staticmethod
    def mark_down():
        self.videotools[3].border_detector.isPressMarkUpButton = False
        print('Button clicked ', self.videotools[3].border_detector.isPressMarkUpButton)
        cv2.destroyAllWindows()

    def start_video(self):
        vsrcs = [None for i in range(CAMERAS_COUNT)]
        videosource = 'cameras'
        if len(sys.argv) > 1:
            videosource = sys.argv[1]

        if (videosource == 'files'):
            vsrcs[0] = '../cat.mp4'
            vsrcs[1] = '../cat.mp4'
            vsrcs[2] = '../people.mp4'
            # vsrcs[3] = '../people.mp4'
        else:
            vsrcs[0] = 'rtsp://192.168.1.203:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrcs[1] = 'rtsp://192.168.1.135:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            vsrcs[2] = 'rtsp://192.168.1.163:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            # vsrcs[3] = 0


        model_name = 'faster_rcnn_inception_v2_coco_2018_01_28'  # HERE - название папки с моделью
        model_path = model_name + '/frozen_inference_graph.pb'  # HERE
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        labels = []
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        with open(labels_path) as f:
            labels = f.readlines()
        labels = [s.strip() for s in labels]

        self.videotools = [VideoTool(src=vsrcs[i], init_fc=i) for i in range(CAMERAS_COUNT)]
        for i in range(CAMERAS_COUNT): 
            print(i)
            self.videotools[i].object_detector = ObjectDetector(detection_graph=detection_graph,
                                                     labels=labels,
                                                     classes_to_detect=CLASSES_TO_DETECT,
                                                     confidence_level=CONFIDENCE_LEVEL)
            self.videotools[i].border_detector = BorderDetector()
            self.videotools[i].motion_detector = MotionDetector()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(40)

    def update_video(self):
        for i in range(len(self.videotools)):
            if self.videotools[i].is_displayable() and self.videotools[i].is_playing:
                a = get_image_qt(self.videotools[i].get_smart_frame(self.width_standard), self.width_standard)
                self.video_labels[i].setPixmap(a)
        # if self.videotools[3].is_playing:
        #     self.videotools[3].get_security_detected(self.width_standard)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Вы действительно хотите закрыть охранную систему",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.videotools[0].object_detector.close()
            for i in range(len(self.videotools)):
                self.videotools[i].close()
            # self.videotools[3].video.release()
            event.accept()
        else:
            event.ignore()

    def video_one_change_mode(self, value):
        self.change_mod_by_mod(value, self.videotools[0])

    def video_two_change_mode(self, value):
        self.change_mod_by_mod(value, self.videotools[1])

    def video_three_change_mode(self, value):
        self.change_mod_by_mod(value, self.videotools[2])

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


"""class Video:
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
            _, frame = self.video.read()
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
            self.mode = state"""

starttime = datetime.now()
global lasttime

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    splash = Splash()
    splash.show()
    window = UI()  # Создаём объект класса ExampleApp
    window.videotools[0].object_detector.process(np.zeros((1, 1, 3)))

    #window.setWindowOpacity(0.5)
    # pal = window.palette()
    # pal.setBrush(QPalette.Normal, QPalette.Background,
    #              QBrush(QPixmap("Fone.jpg")))
    # window.setPalette(pal)
    # window.setAutoFillBackground(True)
    window.show()  # Показываем окно
    splash.finish(window)
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()