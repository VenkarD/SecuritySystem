from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cameramode

class ToolbarButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('font: 10pt "MS Shell Dlg 2";\ncolor: #F0F8FD;\nbackground-image: url(:/everything/resources/buttonBK.jpg);')
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sp.setHorizontalStretch(1)
        self.setSizePolicy(sp)


class ToolbarComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setStyleSheet('font: 10pt "MS Shell Dlg 2";\ncolor: rgb(255, 255, 255);\nbackground-image: url(:/everything/resources/buttonBK.jpg);')
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sp.setHorizontalStretch(2)
        self.setSizePolicy(sp)


class VideoView(QWidget):
    """caption_font = QFont()
    caption_font.setFamily('Arial')
    caption_font.setPointSize(20)"""
    layout_spacing = 4

    def __init__(self, parent, **kwargs):
        QWidget.__init__(self, parent)
        if kwargs is None:
            kwargs = {}

        self.caption = kwargs['caption'] if 'caption' in kwargs else 'Камера'

        self.main_vbox = QVBoxLayout(self)
        self.main_vbox.setSpacing(self.layout_spacing)
        self.caption_label = QLabel(self)
        # self.caption_label.setFont(self.caption_font)
        self.caption_label.setStyleSheet('font-size: 16pt "MS Shell Dlg 2";\ncolor: #F0F8FD;')
        self.caption_label.setText(self.caption)
        self.main_vbox.addWidget(self.caption_label)
        self.video_label_container = QWidget(self)
        self.video_label_container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.video_label_container.setMinimumSize(30, 20)  # например
        self.video_label_container.setStyleSheet('background: black;')
        self.video_label_container_layout = QHBoxLayout(self.video_label_container)
        self.video_label_container_layout.setAlignment(Qt.AlignCenter)
        self.video_label_container_layout.setContentsMargins(0, 0, 0, 0)
        self.video_label = QLabel(self.video_label_container)
        # self.video_label.setStyleSheet('background-image: url(:/everything/resources/Black_bk.jpg);'')
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        # self.video_label.setStyleSheet('background: red;')
        self.video_label_container_layout.addWidget(self.video_label)
        self.main_vbox.addWidget(self.video_label_container)
        self.toolbar_hbox_w = QWidget(self)
        self.toolbar_hbox_w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toolbar_hbox_w.setFixedHeight(25)
        # self.toolbar_hbox_w.setStyleSheet('background: red;')  # debug
        self.toolbar_hbox = QHBoxLayout(self.toolbar_hbox_w)
        self.toolbar_hbox.setSpacing(self.layout_spacing)
        self.toolbar_hbox.setContentsMargins(0, 0, 0, 0)
        self.mode_cb = ToolbarComboBox(self)
        for i in range(5): self.mode_cb.addItem('NONAME')
        self.mode_cb.setItemText(cameramode.ORIGINAL, 'Оригинальный видеопоток')
        self.mode_cb.setItemText(cameramode.DETECT_OBJECTS, 'Обнаружение объектов')
        self.mode_cb.setItemText(cameramode.DETECT_MOTION, 'Обнаружение движения')
        self.mode_cb.setItemText(cameramode.DETECT_VEHICLES, 'Обнаружение транспорта')
        self.mode_cb.setItemText(cameramode.RECOGNIZE_FACES, 'Распознавание лиц')
        # self.mode_cb.setItemText(cameramode.DETECT_BORDERS, 'Обнаружение пересечения границ')
        self.toolbar_hbox.addWidget(self.mode_cb)
        self.borders_btn = ToolbarButton(self)
        self.borders_btn.setText('Обозначить границы')
        self.toolbar_hbox.addWidget(self.borders_btn)
        self.videos_btn = ToolbarButton(self)
        self.videos_btn.setText('Просмотр видео')
        self.toolbar_hbox.addWidget(self.videos_btn)
        self.main_vbox.addWidget(self.toolbar_hbox_w)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
