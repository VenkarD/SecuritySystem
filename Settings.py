# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Form")
        Settings.resize(937, 657)
        #Settings.setStyleSheet("background-image: url(:/newPrefix/Settings.jpg);")

        # Создаем фон настроек
        oImage = QtGui.QImage("Settings.jpg")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(oImage))
        self.setPalette(palette)

        self.brightnessButton = QtWidgets.QPushButton(Settings)
        self.brightnessButton.setGeometry(QtCore.QRect(70, 160, 301, 91))
        self.brightnessButton.setObjectName("brightnessButton")
        self.brightnessButton.setStyleSheet("background-color:transparent;border:0;")
        self.sharpnessButton = QtWidgets.QPushButton(Settings)
        self.sharpnessButton.setGeometry(QtCore.QRect(70, 270, 301, 91))
        self.sharpnessButton.setObjectName("sharpnessButton")
        self.sharpnessButton.setStyleSheet("background-color:transparent;border:0;")
        self.contrastButton = QtWidgets.QPushButton(Settings)
        self.contrastButton.setGeometry(QtCore.QRect(70, 380, 301, 91))
        self.contrastButton.setObjectName("contrastButton")
        self.contrastButton.setStyleSheet("background-color:transparent;border:0;")
        self.colorButton = QtWidgets.QPushButton(Settings)
        self.colorButton.setGeometry(QtCore.QRect(70, 480, 301, 91))
        self.colorButton.setObjectName("colorButton")
        self.colorButton.setStyleSheet("background-color:transparent;border:0;")
        self.returnButton = QtWidgets.QPushButton(Settings)
        self.returnButton.setGeometry(QtCore.QRect(874, 10, 51, 51))
        self.returnButton.setObjectName("returnButton")
        self.returnButton.setStyleSheet("background-color:transparent;border:0;")
        self.radioButtonOn = QtWidgets.QRadioButton(Settings)
        self.radioButtonOn.setGeometry(QtCore.QRect(620, 290, 16, 21))
        self.radioButtonOn.setObjectName("radioButtonOn")
        self.radioButtonAuto = QtWidgets.QRadioButton(Settings)
        self.radioButtonAuto.setGeometry(QtCore.QRect(720, 290, 16, 21))
        self.radioButtonAuto.setObjectName("radioButtonAuto")
        self.radioButtonOff = QtWidgets.QRadioButton(Settings)
        self.radioButtonOff.setGeometry(QtCore.QRect(830, 290, 16, 21))
        self.radioButtonOff.setObjectName("radioButtonOff")

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Form", "Form"))
        self.brightnessButton.setText(_translate("Form", ""))
        self.sharpnessButton.setText(_translate("Form", ""))
        self.contrastButton.setText(_translate("Form", ""))
        self.colorButton.setText(_translate("Form", ""))
        self.returnButton.setText(_translate("Form", ""))
        self.radioButtonOn.setText(_translate("Form", ""))
        self.radioButtonAuto.setText(_translate("Form", ""))
        self.radioButtonOff.setText(_translate("Form", ""))

import xz_rc
