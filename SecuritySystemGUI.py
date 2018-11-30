# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SecuritySystemGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1935, 1071)
        #Form.setStyleSheet("background-image: url(:/newPrefix/Fone.jpg);")

        # Создаем фон приложения
        oImage = QtGui.QImage("Fone.jpg")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(oImage))
        self.setPalette(palette)

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(160, 0, 391, 61))
        self.pushButton_6.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_6.setAcceptDrops(False)
        self.pushButton_6.setToolTipDuration(-1)
#         self.pushButton_6.setStyleSheet("background-image: url(:/newPrefix/buttonBK.jpg);\n"
# "font: 14pt \"MS Shell Dlg 2\";\n"
# "color: rgb(255, 255, 255);")
        self.pushButton_6.setStyleSheet("background-color:transparent;border:0;")
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(564, 2, 391, 61))
#         self.pushButton_7.setStyleSheet("background-image: url(:/newPrefix/buttonBK.jpg);\n"
# "font: 14pt \"MS Shell Dlg 2\";\n"
# "color: rgb(255, 255, 255);")
        self.pushButton_7.setStyleSheet("background-color:transparent;border:0;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(964, 2, 391, 61))
#         self.pushButton_8.setStyleSheet("background-image: url(:/newPrefix/buttonBK.jpg);\n"
# "font: 14pt \"MS Shell Dlg 2\";\n"
# "color: rgb(255, 255, 255);")
        self.pushButton_8.setStyleSheet("background-color:transparent;border:0;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(1360, 2, 391, 61))
#         self.pushButton_9.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
# "color: rgb(255, 255, 255);\n"
# "background-image: url(:/newPrefix/buttonBK.jpg);")
        self.pushButton_9.setStyleSheet("background-color:transparent;border:0;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.video_1 = QtWidgets.QLabel(Form)
        self.video_1.setEnabled(True)
        self.video_1.setGeometry(QtCore.QRect(30, 90, 901, 431))
        palette = QtGui.QPalette()
        self.video_1.setPalette(palette)
        self.video_1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.video_1.setAutoFillBackground(False)
        self.video_1.setStyleSheet("\n"
"background-image: url(:/newPrefix/Black_bk.jpg);")
        self.video_1.setObjectName("video_1")
        self.video_2 = QtWidgets.QLabel(Form)
        self.video_2.setGeometry(QtCore.QRect(980, 90, 901, 431))
        self.video_2.setStyleSheet("background-image: url(:/newPrefix/Black_bk.jpg);")
        self.video_2.setObjectName("video_2")
        self.video_3 = QtWidgets.QLabel(Form)
        self.video_3.setGeometry(QtCore.QRect(20, 600, 1641, 431))
        self.video_3.setStyleSheet("background-image: url(:/newPrefix/Black_bk.jpg);")
        self.video_3.setObjectName("video_3")
        self.comboBox_1 = QtWidgets.QComboBox(Form)
        self.comboBox_1.setGeometry(QtCore.QRect(30, 530, 211, 21))
        self.comboBox_1.setMaximumSize(QtCore.QSize(16777215, 25))
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.pushButton_1 = QtWidgets.QPushButton(Form)
        self.pushButton_1.setGeometry(QtCore.QRect(250, 530, 161, 21))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        #self.pushButton_1.setIcon(QtGui.QIcon("ButtonBK_2.jpg"))
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 530, 161, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(1360, 530, 161, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(1190, 530, 161, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(980, 530, 201, 21))
        self.comboBox_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(1690, 790, 161, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        #self.pushButton_5.setStyleSheet("background-color:transparent;border:0;")
        self.pushButton_5.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(1690, 840, 161, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setStyleSheet("background-image : url(:/newPrefix/ButtonBK_2.jpg); color: white;")
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(1690, 890, 161, 21))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_6.setText(_translate("Form", "")) # Лог оператора
        self.pushButton_7.setText(_translate("Form", "")) # Обновить
        self.pushButton_8.setText(_translate("Form", "")) # Настройки
        self.pushButton_9.setText(_translate("Form", "")) # Выход
        self.video_1.setText(_translate("Form", "TextLabel"))
        self.video_2.setText(_translate("Form", "TextLabel"))
        self.video_3.setText(_translate("Form", "TextLabel"))
        self.comboBox_1.setItemText(0, _translate("Form", "Обычный режим"))
        self.comboBox_1.setItemText(1, _translate("Form", "Распознавание людей"))
        self.comboBox_1.setItemText(2, _translate("Form", "Распознавание движения"))
        self.comboBox_1.setItemText(3, _translate("Form", "Распознавание границ"))
        self.pushButton_1.setText(_translate("Form", "Обозначить Границы"))
        self.pushButton_2.setText(_translate("Form", "Просмотр видео"))
        self.pushButton_4.setText(_translate("Form", "Просмотр видео"))
        self.pushButton_3.setText(_translate("Form", "Обозначить Границы"))
        self.comboBox_2.setItemText(0, _translate("Form", "Обычный режим"))
        self.comboBox_2.setItemText(1, _translate("Form", "Распознавание людей"))
        self.comboBox_2.setItemText(2, _translate("Form", "Распознавание движения"))
        self.comboBox_2.setItemText(3, _translate("Form", "Распознавание границ"))
        self.pushButton_5.setText(_translate("Form", "Просмотр видео"))
        self.pushButton_10.setText(_translate("Form", "Просмотр видео"))
        self.comboBox_3.setItemText(0, _translate("Form", "Обычный режим"))
        self.comboBox_3.setItemText(1, _translate("Form", "Распознавание людей"))
        self.comboBox_3.setItemText(2, _translate("Form", "Распознавание движения"))
        self.comboBox_3.setItemText(3, _translate("Form", "Распознавание границ"))

import xz_rc
