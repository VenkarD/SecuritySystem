# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsForm(object):
    def setupUi(self, SettingsForm):
        SettingsForm.setObjectName("SettingsForm")
        SettingsForm.resize(937, 657)
        SettingsForm.setStyleSheet("background-image: url(:/everything/resources/settings.jpg);")
        self.brightnessButton = QtWidgets.QPushButton(SettingsForm)
        self.brightnessButton.setGeometry(QtCore.QRect(70, 160, 301, 91))
        self.brightnessButton.setObjectName("brightnessButton")
        self.sharpnessButton = QtWidgets.QPushButton(SettingsForm)
        self.sharpnessButton.setGeometry(QtCore.QRect(70, 270, 301, 91))
        self.sharpnessButton.setObjectName("sharpnessButton")
        self.contrastButton = QtWidgets.QPushButton(SettingsForm)
        self.contrastButton.setGeometry(QtCore.QRect(70, 380, 301, 91))
        self.contrastButton.setObjectName("contrastButton")
        self.colorButton = QtWidgets.QPushButton(SettingsForm)
        self.colorButton.setGeometry(QtCore.QRect(70, 480, 301, 91))
        self.colorButton.setObjectName("colorButton")
        self.returnButton = QtWidgets.QPushButton(SettingsForm)
        self.returnButton.setGeometry(QtCore.QRect(874, 10, 51, 51))
        self.returnButton.setObjectName("returnButton")
        self.radioButtonOn = QtWidgets.QRadioButton(SettingsForm)
        self.radioButtonOn.setGeometry(QtCore.QRect(620, 290, 16, 21))
        self.radioButtonOn.setObjectName("radioButtonOn")
        self.radioButtonAuto = QtWidgets.QRadioButton(SettingsForm)
        self.radioButtonAuto.setGeometry(QtCore.QRect(720, 290, 16, 21))
        self.radioButtonAuto.setObjectName("radioButtonAuto")
        self.radioButtonOff = QtWidgets.QRadioButton(SettingsForm)
        self.radioButtonOff.setGeometry(QtCore.QRect(830, 290, 16, 21))
        self.radioButtonOff.setChecked(True)
        self.radioButtonOff.setObjectName("radioButtonOff")

        self.retranslateUi(SettingsForm)
        QtCore.QMetaObject.connectSlotsByName(SettingsForm)

    def retranslateUi(self, SettingsForm):
        _translate = QtCore.QCoreApplication.translate
        SettingsForm.setWindowTitle(_translate("SettingsForm", "Form"))
        self.brightnessButton.setText(_translate("SettingsForm", "PushButton"))
        self.sharpnessButton.setText(_translate("SettingsForm", "PushButton"))
        self.contrastButton.setText(_translate("SettingsForm", "PushButton"))
        self.colorButton.setText(_translate("SettingsForm", "PushButton"))
        self.returnButton.setText(_translate("SettingsForm", "PushButton"))
        self.radioButtonOn.setText(_translate("SettingsForm", "RadioButton"))
        self.radioButtonAuto.setText(_translate("SettingsForm", "RadioButton"))
        self.radioButtonOff.setText(_translate("SettingsForm", "RadioButton"))

import xz_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsForm = QtWidgets.QWidget()
    ui = Ui_SettingsForm()
    ui.setupUi(SettingsForm)
    SettingsForm.show()
    sys.exit(app.exec_())

