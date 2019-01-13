import cv2
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets


def imageToPixmap(image):
    height = np.shape(image)[0]
    totalBytes = image.nbytes
    bytesPerLine = int(totalBytes / height)
    qimg = QtGui.QImage(image.data, image.shape[1], image.shape[0], bytesPerLine, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qimg)


class QImageButton(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(bool)

    def __init__(self, parent):
        QtWidgets.QLabel.__init__(self, parent)
        self.pixmapEnabled = None
        self.pixmapDisabled = None

    def mousePressEvent(self, event):
        self.clicked.emit(False)

    def setImage(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.pixmapEnabled = imageToPixmap(image)
        self.pixmapDisabled = imageToPixmap(gray_image)
        self.updatePixmap()

    def setEnabled(self, isEnabled):
        QtWidgets.QLabel.setEnabled(self, isEnabled)
        self.updatePixmap()

    def updatePixmap(self):
        self.setPixmap(self.pixmapEnabled if self.isEnabled() else self.pixmapDisabled)
