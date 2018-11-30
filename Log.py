# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Log.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Log(object):
    def setupUi(self, Log):
        Log.setObjectName("Form")
        Log.resize(645, 727)
        #Log.setStyleSheet("background-image: url(:/newPrefix/Log.jpg);")

        # Создаем фон приложения
        oImage = QtGui.QImage("Log.jpg")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(oImage))
        self.setPalette(palette)

        self.pushButton = QtWidgets.QPushButton(Log)
        self.pushButton.setGeometry(QtCore.QRect(584, 30, 51, 41))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("background-color:transparent;border:0;")
        self.textEdit = QtWidgets.QTextEdit(Log)
        self.textEdit.setGeometry(QtCore.QRect(20, 110, 611, 571))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Log)
        QtCore.QMetaObject.connectSlotsByName(Log)

    def retranslateUi(self, Log):
        _translate = QtCore.QCoreApplication.translate
        Log.setWindowTitle(_translate("Form", "Form"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

import xz_rc
