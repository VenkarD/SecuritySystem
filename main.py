import logging
import sys
import time
import traceback
import gc

import cv2
import tensorflow as tf
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime

from threading import Thread, Lock, Event

#import design
import mainwindow
import settings
import log
from custom_widgets.QImageButton import QImageButton

import cameramode
from videotool import VideoTool
from videoview import VideoView
from frame_analysis.object_detector import ObjectDetector
from frame_analysis.border_detector import BorderDetector, Region
from frame_analysis.motion_detector import MotionDetector
from frame_analysis.face_recognizer import FaceRecognizer

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
CLASSES_TO_DETECT_MANCATDOG = [
    1,      # person
    17,     # cat
    18      # dog
]
CLASSES_TO_DETECT_VEHICLES = [
    2,      #bicycle
    3,      #car
    4,      #motorcycle
    6,      #bus
    8,      #truck
]  # HERE - классы для обнаружения, см. файл classes_en.txt
   # номер класса = номер строки, нумерация с 1


def get_image_qt(frame):
    # решает проблему с искажением кадров
    height, width, channels = np.shape(frame)
    totalBytes = frame.nbytes
    bytesPerLine = int(totalBytes / height)

    qimg = QImage(frame.data, frame.shape[1], frame.shape[0], bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


class ModuleSettingsKit:
    def __init__(self, name, widget_page):
        self.name = name
        self.widget_page = widget_page


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


# Окно Настроек
class SettingsWindow(QWidget, settings.Ui_SettingsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Settings')
        self.returnButton.clicked.connect(self.returnToMain)
        self.setWindowIcon(QIcon("icon_settings.png"))

    def returnToMain(self, event):
        self.close()
        self.destroy()


# Окно Log'a
class LogWindow(QWidget, log.Ui_Log):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Log')
        self.pushButton.clicked.connect(self.returnToMain)
        self.setWindowIcon(QIcon("icon_log.png"))

    def returnToMain(self, event):
        self.close()
        self.destroy()


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


class VideoWorker(Thread):
    def __init__(self, idx, name, video_source, vv_positions, videotools, videoviews,
                 mutexes, stop_event, parent_window, cameras_layout, known_face_encodings,
                 known_face_names, detection_graph, labels):
        super().__init__(name=name)

        def on_mode_cb_changed(index):
            if index == cameramode.DETECT_OBJECTS:
                self.vtool.object_detector.classes_to_detect = CLASSES_TO_DETECT_MANCATDOG
            elif index == cameramode.DETECT_VEHICLES:
                self.vtool.object_detector.classes_to_detect = CLASSES_TO_DETECT_VEHICLES
            self.vtool.set_mode(index)


        def borders_slot(event):
            # self.mutex.acquire()  # cv2.imshow() не дружит с многопоточностью
            if self.vtool.border_detector.is_drawing:
                self.vtool.border_detector.end_selecting_region()
                self.vtool.is_borders_mode = len(self.vtool.border_detector.regions) > 0
                self.vview.borders_btn.setText('Добавить границы')
                self.vview.borders_clear_btn.setEnabled(True)
            else:
                self.vview.video_label.pixmap().fill(QColor(0, 0, 0))
                new_region = Region("New Region")
                self.vtool.border_detector.add_region(new_region)
                self.vtool.border_detector.start_selecting_region(\
                        new_region, str(datetime.now()))
                self.vview.borders_btn.setText('Сохранить границы')
                self.vview.borders_clear_btn.setEnabled(False)
            # self.mutex.release()

        def borders_clear_slot(event):
            vtool = self.vtool
            vview = self.vview

            # self.mutex.acquire()  # cv2.imshow() не дружит с многопоточностью
            vtool.border_detector.clear_regions()
            vtool.is_borders_mode = False
            # self.mutex.release()

        self.videoviews = videoviews
        if self.videoviews is not None:
            self.vview = VideoView(parent_window, caption='Камера №'+str(idx+1))
            self.videoviews.append(self.vview)
            row, col, w, h = vv_positions
            self.cameras_layout = cameras_layout
            self.cameras_layout.addWidget(self.vview, row, col, h, w)
            self.vview.mode_cb.currentIndexChanged.connect(on_mode_cb_changed)
            self.vview.borders_btn.clicked.connect(borders_slot)
            self.vview.borders_clear_btn.clicked.connect(borders_clear_slot)

        self.vtool = VideoTool(src=video_source, init_fc=idx)
        self.mutex = Lock()
        self.stop_event = stop_event

        self.emergency_stop = False
        self.last_frame = None
        self.reader = Thread(target=self.read_stream, args=[stop_event])
        """ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"ф"""

        self.videotools = videotools
        self.videotools.append(self.vtool)
        self.vtool.object_detector = ObjectDetector(detection_graph=detection_graph,
                                                    labels=labels,
                                                    classes_to_detect=CLASSES_TO_DETECT_MANCATDOG,
                                                    confidence_level=CONFIDENCE_LEVEL)
        self.vtool.border_detector = BorderDetector()
        self.vtool.motion_detector = MotionDetector()
        self.vtool.face_recognizer = FaceRecognizer(known_face_encodings, known_face_names)

        self.mutexes = mutexes
        self.mutexes.append(self.mutex)

    def read_stream(self, stop_event):
        print('{}: let\'s read the stream!'.format(self.getName()))
        try:
            while not stop_event.is_set() and not self.emergency_stop:
                ret, self.last_frame = self.vtool.video.read()
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
        print('{}: done!'.format(self.getName()))

    def run(self):
        self.reader.start()
        try:
            while not self.stop_event.wait(timeout=0.001):
            # while not self.stop_event.is_set():
                # time_start = datetime.now()
                self.mutex.acquire()
                if not self.stop_event.is_set() and self.last_frame is not None:
                    self.tick()
                self.mutex.release()
                # elapsed_ms = (datetime.now() - time_start).microseconds / 1000
                # print(elapsed_ms, 'ms elapsed')
                # time.sleep(max(0, self.vtool.freq_ms - elapsed_ms) / 1000)
            print('It\'s {}, goodbye!'.format(self.getName()))
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
            self.emergency_stop = True
            if self.mutex.locked():
                self.mutex.release()
        self.reader.join()
        self.on_stop()

    # Действия, которые выполняются над каждым кадром
    def tick(self):
        if self.vtool.is_displayable() and self.vtool.is_playing:
            container = self.vview.video_label_container

            geometry = container.geometry()
            ratio_w = geometry.width() / self.vtool.frame_w
            ratio_h = geometry.height() / self.vtool.frame_h
            ratio = min(ratio_w, ratio_h)
            # print(ratio)

            if self.vtool.border_detector.is_drawing:
                frame = self.vtool.get_frame(self.last_frame,
                                             int(self.vtool.frame_w * ratio),
                                             int(self.vtool.frame_h * ratio),
                                             mode=cameramode.ORIGINAL,
                                             bgr_to_rgb=False)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow(self.vtool.border_detector.window_id,
                           self.vtool.border_detector.draw_regions(frame,
                           self.vtool.color_bad,
                           self.vtool.thickness_border))
                """if cv2.waitKey(self.vtool.freq_ms) == ord('q'):  # ??? HOWTO?
                    print('qq!')
                    self.vview.borders_btn.click()"""
            else:
                frame = self.vtool.get_frame(self.last_frame,
                                             int(self.vtool.frame_w * ratio),
                                             int(self.vtool.frame_h * ratio))
                frame = get_image_qt(frame)
                self.vview.video_label.setPixmap(frame)

    def start(self):
        print('Hello, I\'m {}'.format(self.getName()))
        self.emergency_stop = False
        super().start()

    # Выполняется один раз при корректном завершении работы потока
    def on_stop(self):
        self.vtool.close()
        self.mutexes.remove(self.mutex)
        self.videotools.remove(self.vtool)
        if self.videoviews is not None:
            self.videoviews.remove(self.vview)
            self.cameras_layout.removeWidget(self.vview)
            self.vview.deleteLater()
            self.vview = None


class SecurityDetectorWorker(Thread):
    def __init__(self, name, video_capture, object_detector,
                 checking_period_sec, checking_burst, mutex, stop_event):
        super().__init__(name=name)
        self.video_capture = video_capture
        self.object_detector = object_detector
        self.checking_period_sec = checking_period_sec
        self.checking_burst = checking_burst
        self.mutex = mutex
        self.stop_event = stop_event

        self.security_prev_state = False
        self.security_curr_state = False
    
    def run(self):
        try:
            self.tick()
            while not self.stop_event.is_set():
                waiting_start_time = datetime.now()
                while (datetime.now() - waiting_start_time).seconds < self.checking_period_sec:
                    self.video_capture.read()
                    if self.stop_event.is_set():
                        break;
                # time_start = datetime.now()
                self.mutex.acquire()
                if not self.stop_event.is_set():
                    self.tick()
                self.mutex.release()
                # elapsed_ms = (datetime.now() - time_start).microseconds / 1000
                # print(elapsed_ms, 'ms elapsed')
                # time.sleep(max(0, self.vtool.freq_ms - elapsed_ms) / 1000)
            print('It\'s {}, goodbye!'.format(self.getName()))
        except:
            print('{} - unexpected error: {}'.format(self.getName(), traceback.format_exc()))
            if self.mutex.locked():
                self.mutex.release()

    # Действия, которые выполняются над каждым кадром
    def tick(self):
        print('Let\'s check...')
        self.security_prev_state = self.security_curr_state
        self.security_curr_state = False
        log_str = ''
        for i in range(self.checking_burst):
            if self.stop_event.is_set():
                return

            frame = self.video_capture.read()[1]
            boxes, scores, classes = self.object_detector.process(frame)
            if len(boxes) > 0:
                self.security_curr_state = True
                break

        if self.security_curr_state != self.security_prev_state:
            log_str = '{} - охранник {}'.format(datetime.now().\
                    strftime('%d.%m.%y %H:%M'),\
                    'на месте' if self.security_curr_state else 'отсутствует')

        print('Log:', log_str)
        if(log_str != ''):
            with open('log.txt', 'a') as f:
                f.write(log_str + '\r\n')

    def start(self):
        print('Hello, I\'m {}'.format(self.getName()))
        super().start()



class UI(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.image = None
        self.width_standard = 1200
        self.width360 = 1600

        self.vsrcs = [None] * 4
        secsrc = None
        videosource = 'cameras'
        if len(sys.argv) > 1:
            videosource = sys.argv[1]

        if (videosource == 'files'):
            self.vsrcs[0] = '../people.mp4'
            self.vsrcs[1] = '../cat.mp4'
            self.vsrcs[2] = '../people.mp4'
            self.vsrcs[3] = '../people.mp4'
            secsrc = '../people.mp4'
        else:
            self.vsrcs[0] = 'rtsp://192.168.1.192:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            self.vsrcs[1] = 'rtsp://192.168.1.239:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            self.vsrcs[2] = 'rtsp://192.168.1.163:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
            self.vsrcs[3] = 0
            secsrc = 0

        self.vv_positions = [(1, 1, 1, 1),  # Позиции создаваемых VideoView в сетке
                        (1, 2, 1, 1),  # (строка, столбец, ширина, высота)
                        (2, 1, 2 if CAMERAS_COUNT == 3 else 1, 1),
                        (2, 2, 1, 1)
                       ]

        model_name = 'nn_model'  # faster_rcnn_inception_v2_coco_2018_01_28
        model_path = model_name + '/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.labels = []
        labels_path = 'classes_en.txt'  # HERE - файл с подписями для классов
        with open(labels_path) as f:
            self.labels = f.readlines()
        self.labels = [s.strip() for s in self.labels]

        # Фотографии и имена для распознавания лиц
        # TODO: работать через БД
        faces_folder = 'faces'
        self.known_face_photos = [
            'Bogdan.jpg', 
            'Bogdan_1.jpg',
            'Egor_2.jpg',
            'Tima.jpg',
            'Tima_1.jpg',
            'Tima_2.jpg',
            'biden.jpg'
        ]
        self.known_face_encodings = [FaceRecognizer.get_face_encoding(cv2.imread(
                                faces_folder + '/' + face)) 
                                for face in self.known_face_photos]
        self.known_face_names = [
            "Bogdan",
            "Bogdan",
            "Egor",
            "Tima",
            "Tima",
            "Tima"
        ]

        # Инициализация инструментария для каждого видеопотока
        self.videotools = []
        self.videoviews = []
        self.mutexes = []

        # TODO: перенести создание объектов в потоки
        self.stop_cam_threads_event = Event()

        for i in range(CAMERAS_COUNT):
            """self.videotools.append(VideoTool(src=vsrcs[i], init_fc=i))
            self.videotools[i].object_detector = ObjectDetector(detection_graph=detection_graph,
                                                                labels=labels,
                                                                classes_to_detect=CLASSES_TO_DETECT_MANCATDOG,
                                                                confidence_level=CONFIDENCE_LEVEL)
            self.videotools[i].border_detector = BorderDetector()
            self.videotools[i].motion_detector = MotionDetector()
            self.videotools[i].face_recognizer = FaceRecognizer(known_face_encodings, known_face_names)

            self.videoviews.append(VideoView(self, caption='Камера №'+str(i+1)))
            row, col, w, h = vv_positions[i]
            self.cameras_layout.addWidget(self.videoviews[i], row, col, h, w)

            def on_mode_cb_changed(index, i=i):
                if index == cameramode.DETECT_OBJECTS:
                    self.videotools[i].object_detector.classes_to_detect = CLASSES_TO_DETECT_MANCATDOG
                elif index == cameramode.DETECT_VEHICLES:
                    self.videotools[i].object_detector.classes_to_detect = CLASSES_TO_DETECT_VEHICLES
                self.videotools[i].set_mode(index)

            self.videoviews[i].mode_cb.currentIndexChanged.\
                    connect(on_mode_cb_changed)

            def borders_slot(event, i=i):
                vtool = self.videotools[i]
                vview = self.videoviews[i]

                # self.mutexes[i].acquire()  # cv2.imshow() не дружит с многопоточностью
                if vtool.border_detector.is_drawing:
                    vtool.border_detector.end_selecting_region()
                    vtool.is_borders_mode = len(vtool.border_detector.regions) > 0
                    vview.borders_btn.setText('Добавить границы')
                    vview.borders_clear_btn.setEnabled(True)
                else:
                    vview.video_label.pixmap().fill(QColor(0, 0, 0))
                    new_region = Region("New Region")
                    vtool.border_detector.add_region(new_region)
                    vtool.border_detector.start_selecting_region(\
                            new_region, str(datetime.now()))
                    vview.borders_btn.setText('Сохранить границы')
                    vview.borders_clear_btn.setEnabled(False)
                # self.mutexes[i].release()
            self.videoviews[i].borders_btn.clicked.connect(borders_slot)

            def borders_clear_slot(event, i=i):
                vtool = self.videotools[i]
                vview = self.videoviews[i]

                # self.mutexes[i].acquire()  # cv2.imshow() не дружит с многопоточностью
                vtool.border_detector.clear_regions()
                vtool.is_borders_mode = False
                # self.mutexes[i].release()
            self.videoviews[i].borders_clear_btn.clicked.connect(borders_clear_slot)
            self.mutexes.append(Lock())"""

        # self.security_capture = cv2.VideoCapture(secsrc)
        """self.security_detector = ObjectDetector(detection_graph=detection_graph,
                                                labels=labels,
                                                classes_to_detect=[1],  # person
                                                confidence_level=CONFIDENCE_LEVEL)"""
        self.security_mutex = Lock()
        self.stop_security_event = Event()

        self.setWindowTitle('Security System')
        self.settings_window = None
        self.log_window = None
        self.prepare_settings_form()
        self.setup_handlers()

    def prepare_settings_form(self):
        # TODO: назначить соответствующие иконки
        add_img = cv2.imread('resources/add.png')
        self.add_zone_btn.setImage(add_img)
        self.add_camera_btn.setImage(add_img)
        self.rename_zone_camera_btn.setImage(add_img)
        self.remove_zone_camera_btn.setImage(add_img)

        self.module_kits = [ModuleSettingsKit('Объекты', self.detect_objects_settings_page),
                            ModuleSettingsKit('Движение', self.detect_motion_settings_page),
                            ModuleSettingsKit('Лица', self.recognize_faces_settings_page),
                            ModuleSettingsKit('Номерные знаки', self.recognize_license_plates_settings_page),
                            ModuleSettingsKit('Границы', self.detect_borders_settings_page)]
        for kit in self.module_kits:
            item = QListWidgetItem(kit.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.modules_listview.addItem(item)

    def setup_handlers(self):
        self.cameras_btn.clicked.connect(self.show_cameras_page)
        self.refresh_btn.clicked.connect(self.refresh_cameras)
        # self.refresh_btn.clicked.connect(self.refresh_security_cam)
        self.settings_btn.clicked.connect(self.show_settings_page)
        self.log_btn.clicked.connect(self.log_open)
        self.exit_btn.clicked.connect(self.close)

        # TODO: таг, если тут закомментировано, то откуда прога знает что делать по клику?
        # self.add_zone_btn.clicked.connect(self.on_add_zone_btn_clicked)
        # self.add_camera_btn.clicked.connect(self.on_add_camera_btn_clicked)
        # self.rename_zone_camera_btn.clicked.connect(self.on_rename_zone_camera_btn_clicked)

    # Запускает обработку всех видеопотоков в отдельных потоках выполнения
    def start_cam_threads(self):
        self.cam_threads = []
        for i in range(CAMERAS_COUNT):
            """self.cam_threads.append(VideoWorker('VideoWorker' + str(i),
                                                self.videotools[i],
                                                self.videoviews[i],
                                                self.mutexes[i],
                                                self.stop_cam_threads_event))"""
            self.cam_threads.append(VideoWorker(idx=i,
                                                name='VideoWorker' + str(i),
                                                video_source=self.vsrcs[i],
                                                vv_positions=self.vv_positions[i],
                                                videotools=self.videotools,
                                                videoviews=self.videoviews,
                                                mutexes=self.mutexes,
                                                stop_event=self.stop_cam_threads_event,
                                                parent_window=self,
                                                cameras_layout=self.cameras_layout,
                                                known_face_encodings=self.known_face_encodings,
                                                known_face_names=self.known_face_names,
                                                detection_graph=self.detection_graph,
                                                labels=self.labels))
            self.cam_threads[i].start()

    def start_security_thread(self):
        self.security_thread = SecurityDetectorWorker(name='SecurityDetector',
                                                      video_capture=self.security_capture,
                                                      object_detector=self.security_detector,
                                                      checking_period_sec=10,
                                                      checking_burst=5,
                                                      mutex=self.security_mutex,
                                                      stop_event=self.stop_security_event)
        self.security_thread.start()

    # Сообщает всем отдельным потокам выполнения, что обработка больше не нужна
    def stop_cam_threads(self):
        self.stop_cam_threads_event.set()

    def stop_security_thread(self):
        self.stop_security_event.set()

    def stop_cam_threads_and_wait(self):
        self.stop_cam_threads()

        for i in range(CAMERAS_COUNT):
            self.cam_threads[i].join()
            print('Goodbye, {}!'.format(self.cam_threads[i].getName()))
        print('All camera threads are stopped')

    def stop_security_thread_and_wait(self):
        self.stop_security_thread()
        self.security_thread.join()
        print('Goodbye, {}!'.format(self.security_thread.getName()))

    def show_cameras_page(self, event):
        self.stacked_widget.setCurrentWidget(self.cameras_page)

    def show_settings_page(self, event):
        #print("it's realy settingsButton")
        """if not self.settings_window:
            self.settings_window = SettingsWindow()
        self.settings_window.show()"""
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def log_open(self, event):
        if not self.log_window:
            self.log_window = LogWindow()
        self.log_window.show()
        with open("log.txt", 'r') as f:
            mytext = f.read()
            self.log_window.textEdit.setPlainText(mytext)

    def refresh_cameras(self):
        self.stop_cam_threads_and_wait()
        self.stop_cam_threads_event.clear()
        self.start_cam_threads()

    def refresh_security_cam(self):
        self.stop_security_thread_and_wait()
        self.stop_security_event.clear()
        self.start_security_thread()

    def on_add_zone_btn_clicked(self, event):
        name, dialog_result = QInputDialog.getText(self, 'Добавление зоны',
                                            'Введите название зоны:')
        if dialog_result and len(name) > 0:
            QTreeWidgetItem(self.cameras_treeview, [name])

    def on_add_camera_btn_clicked(self, event):
        selected = self.cameras_treeview.selectedItems()[0]
        name, dialog_result = QInputDialog.getText(self, 'Добавление камеры',
                                            'Введите название камеры:')
        if dialog_result and len(name) > 0:
            if selected.parent():
                parent = selected.parent()
            else:
                parent = selected
            item = QTreeWidgetItem(parent, [name])
            item.setFlags(item.flags() | Qt.ItemNeverHasChildren)

    def on_rename_zone_camera_btn_clicked(self, event):
        selected = self.cameras_treeview.selectedItems()[0]
        renaming_of_what = 'камеры' if selected.parent() else 'зоны'
        name, dialog_result = QInputDialog.getText(self, 'Переименование {}'.format(renaming_of_what),
                'Введите название {}:'.format(renaming_of_what))
        if dialog_result and len(name) > 0:
            selected.setText(0, name)

    def on_remove_zone_camera_btn_clicked(self, event):
        selected = self.cameras_treeview.selectedItems()[0]
        removing_of_what = 'камеру' if selected.parent() else 'зону'
        dialog_result = QMessageBox.question(self, 'Подтвердите действие',
                'Вы действительно хотите удалить {} из списка?'.format(removing_of_what),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if dialog_result == QMessageBox.Yes:
            (selected.parent() or self.cameras_treeview.invisibleRootItem()).removeChild(selected)

    def on_modules_listview_currentRowChanged(self, current_row):
        self.module_settings_panel.setCurrentWidget(self.module_kits[current_row].widget_page)

    def closeEvent(self, event):
        dialog_result = QMessageBox.question(self, 'Подтвердите действие',
                'Вы действительно хотите закрыть охранную систему?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if dialog_result == QMessageBox.Yes:
            self.stop_cam_threads_and_wait()
            self.stop_cam_threads_event.clear()

            # for i in range(CAMERAS_COUNT):
                # self.mutexes[i].acquire()
                # self.cam_threads[i].stop_gracefully()
                # self.videotools[i].close()
                # self.mutexes[i].release()

            # self.stop_security_thread_and_wait()
            self.stop_cam_threads_event.clear()
            # self.security_capture.release()
            if len(self.videotools) > 0:
                self.videotools[0].object_detector.close()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    splash = Splash()
    splash.show()
    window = UI()  # Создаём объект класса ExampleApp
    #window.videotools[0].object_detector.process(np.zeros((1, 1, 3)))
    #window.setWindowOpacity(0.5)
    # pal = window.palette()
    # pal.setBrush(QPalette.Normal, QPalette.Background,
    #              QBrush(QPixmap("resources/Fone.jpg")))
    # window.setPalette(pal)
    # window.setAutoFillBackground(True)
    window.start_cam_threads()
    # window.start_security_thread()
    time.sleep(2)
    window.show()  # Показываем окно
    splash.finish(window)
    app.exec_()  # и запускаем прило


if __name__ == '__main__':
    main()