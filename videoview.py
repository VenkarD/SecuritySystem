from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class VideoView(QWidget):
    caption_font = QFont()
    caption_font.setFamily('Arial')
    caption_font.setPointSize(20)
    layout_spacing = 8

    def __init__(self, parent, **kwargs):
        QWidget.__init__(self, parent)
        if kwargs is None:
            kwargs = {}

        self.caption = kwargs['caption'] if 'caption' in kwargs else 'Камера'

        self.main_vbox = QVBoxLayout(self)
        self.main_vbox.setSpacing(self.layout_spacing)
        self.caption_label = QLabel(self)
        self.caption_label.setFont(self.caption_font)
        self.caption_label.setText(self.caption)
        self.main_vbox.addWidget(self.caption_label)
        self.video_label = QLabel(self)
        # self.video_label.setStyleSheet('background-image: url(:/newPrefix/Black_bk.jpg);'')
        self.video_label.setStyleSheet('background: black;')
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_vbox.addWidget(self.video_label)
        self.toolbar_hbox_w = QWidget(self)
        self.toolbar_hbox = QHBoxLayout(self.toolbar_hbox_w)
        self.toolbar_hbox.setSpacing(self.layout_spacing)
        self.mode_cb = QComboBox(self)
        self.mode_cb.addItem('Оригинальынй видеопоток')
        self.mode_cb.addItem('Обнаружение объектов')
        self.mode_cb.addItem('Обнаружение движения')
        self.mode_cb.addItem('Обнаружение пересечения границ')
        self.toolbar_hbox.addWidget(self.mode_cb)
        self.borders_btn = QPushButton(self)
        self.borders_btn.setText('Обозначить границы')
        self.toolbar_hbox.addWidget(self.borders_btn)
        self.videos_btn = QPushButton(self)
        self.videos_btn.setText('Просмотр видео')
        self.toolbar_hbox.addWidget(self.videos_btn)
        self.main_vbox.addWidget(self.toolbar_hbox_w)
