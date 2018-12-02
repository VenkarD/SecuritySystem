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
from videoview import VideoView
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

CAMERAS_COUNT = 1
CONFIDENCE_LEVEL = 0.7  # HERE - нижний порог уверенности модели от 0 до 1.
                        # 0.7 - объект в кадре будет обведён рамкой, если
                        #       сеть уверена на 70% и выше
CLASSES_TO_DETECT = [
    1,      # person
    16,     # cat
    17      # dog
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1


def get_image_qt(frame):
    # решает проблему с искажением кадров
    height, width, channels = np.shape(frame)
    totalBytes = frame.nbytes
    bytesPerLine = int(totalBytes / height)

    qimg = QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)

# Иконка загрузки
class Splash(QSplashScreen):
    def __init__(self, *arg, **args):
        QSplashScreen.__init__(self, *arg, **args)
        self.setCursor(Qt.BusyCursor)
        self.setPixmap(QPixmap("resources/boot.jpg"))
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

class UI(QMainWindow, SecuritySystemGUI.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 1200
        self.width360 = 1600

        vsrcs = [None] * 4
        videosource = 'cameras'
        if len(sys.argv) > 1:
            videosource = sys.argv[1]

        if (videosource == 'files'):
            vsrcs[0] = '../cat.mp4'
            # vsrcs[1] = '../cat.mp4'
            # vsrcs[2] = '../people.mp4'
            # vsrcs[3] = '../people.mp4'
        else:
            vsrcs[0] = 0# 'rtsp://192.168.1.203:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            # vsrcs[1] = 'rtsp://192.168.1.135:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            # vsrcs[2] = 'rtsp://192.168.1.163:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            # vsrcs[3] = 0

        vv_positions = [(1, 1, 1, 1)  # Позиции создаваемых VideoView в сетке
                        # (1, 2, 1, 1),  # (строка, столбец, ширина, высота)
                        # (2, 1, 2 if CAMERAS_COUNT == 3 else 1, 1),
                        # (2, 2, 1, 1)
                        ]

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


        self.videotools = [None] * CAMERAS_COUNT
        self.videoviews = [None] * CAMERAS_COUNT
        for i in range(CAMERAS_COUNT):
            self.videotools[i] = VideoTool(src=vsrcs[i], init_fc=i)
            self.videotools[i].object_detector = ObjectDetector(detection_graph=detection_graph,
                                                                labels=labels,
                                                                classes_to_detect=CLASSES_TO_DETECT,
                                                                confidence_level=CONFIDENCE_LEVEL)
            self.videotools[i].border_detector = BorderDetector()
            self.videotools[i].motion_detector = MotionDetector()

            self.videoviews[i] = VideoView(self, caption='Камера №'+str(i+1))
            row, col, w, h = vv_positions[i]
            self.main_grid.addWidget(self.videoviews[i], row, col, h, w)

            self.videoviews[i].mode_cb.currentIndexChanged.\
                connect(self.videotools[i].set_mode)

            def borders_slot(event, i=i):
                if self.videotools[i].border_detector.isPressMarkUpButton:
                    self.videotools[i].border_detector.end_selecting_region()
                    self.videoviews[i].borders_btn.setText('Обозначить границы')
                else:
                    self.videotools[i].border_detector.start_selecting_region(str(datetime.now()))
                    self.videoviews[i].borders_btn.setText('Деактивировать')

            self.videoviews[i].borders_btn.clicked.connect(borders_slot)
                

        self.start_video()
        self.setWindowTitle('Security System')
        self.settings_btn.clicked.connect(self.setings_open)
        self.exit_btn.clicked.connect(self.close)
        self.secondWin = None
        self.update_video()

    def setings_open(self, event):
        print("it's realy settingsButton")
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()

    def start_video(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(40)

    def update_video(self):
        for i in range(CAMERAS_COUNT):
            if self.videotools[i].is_displayable() and self.videotools[i].is_playing:
                container = self.videoviews[i].video_label_container
                vtool = self.videotools[i]

                ratio_w = container.width() / vtool.frame_w
                ratio_h = container.height() / vtool.frame_h
                ratio = min(ratio_w, ratio_h)
                frame = vtool.get_smart_frame(int(vtool.frame_w * ratio), 
                                              int(vtool.frame_h * ratio))
                frame = get_image_qt(frame)
                # cv2.imwrite(self.videoviews[i].caption + '_testimg.png', frame)
                self.videoviews[i].video_label.setPixmap(frame)

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

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    splash = Splash()
    splash.show()
    window = UI()  # Создаём объект класса ExampleApp
    window.videotools[0].object_detector.process(np.zeros((1, 1, 3)))
    #window.setWindowOpacity(0.5)
    # pal = window.palette()
    # pal.setBrush(QPalette.Normal, QPalette.Background,
    #              QBrush(QPixmap("resources/Fone.jpg")))
    # window.setPalette(pal)
    # window.setAutoFillBackground(True)
    window.show()  # Показываем окно
    splash.finish(window)
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()