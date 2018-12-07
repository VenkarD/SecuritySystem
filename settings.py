# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings__.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setObjectName("Form")
        Form.resize(935, 669)
        Form.setAcceptDrops(False)

        # Создаем фон приложения
        oImage = QtGui.QImage("resources/Norm_Settings.jpg")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(oImage))
        self.setPalette(palette)

        self.returnButton = QtWidgets.QPushButton(Form)
        self.returnButton.setGeometry(QtCore.QRect(864, 10, 51, 51))
        self.returnButton.setText("")
        self.returnButton.setObjectName("returnButton")
        self.returnButton.setStyleSheet("background-color:transparent;border:0;")

        self.NightBRgroupBox = QtWidgets.QGroupBox(Form)
        self.NightBRgroupBox.setGeometry(QtCore.QRect(600, 290, 251, 31))
        self.NightBRgroupBox.setTitle("")
        self.NightBRgroupBox.setObjectName("NightBRgroupBox")
        self.NightBRgroupBox.setStyleSheet("background-color:transparent;border:0;")

        self.nightModeOn = QtWidgets.QRadioButton(self.NightBRgroupBox)
        self.nightModeOn.setGeometry(QtCore.QRect(20, 0, 16, 31))
        self.nightModeOn.setText("")
        self.nightModeOn.setObjectName("nightModeOn")
        self.buttonGroup = QtWidgets.QButtonGroup(Form)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.nightModeOn)
        self.nightModeAuto = QtWidgets.QRadioButton(self.NightBRgroupBox)
        self.nightModeAuto.setGeometry(QtCore.QRect(120, 0, 16, 31))
        self.nightModeAuto.setText("")
        self.nightModeAuto.setObjectName("nightModeAuto")
        self.buttonGroup.addButton(self.nightModeAuto)
        self.nightModeOff = QtWidgets.QRadioButton(self.NightBRgroupBox)
        self.nightModeOff.setGeometry(QtCore.QRect(210, 0, 16, 31))
        self.nightModeOff.setText("")
        self.nightModeOff.setObjectName("nightModeOff")
        self.buttonGroup.addButton(self.nightModeOff)

        #-------------------------------------------------------------
        # Цвет рамок для людей
        # ------------------------------------------------------------
        self.hCRBgroupBox = QtWidgets.QGroupBox(Form)
        self.hCRBgroupBox.setGeometry(QtCore.QRect(50, 200, 281, 71))
        self.hCRBgroupBox.setTitle("")
        self.hCRBgroupBox.setObjectName("hCRBgroupBox")
        self.hCRBgroupBox.setStyleSheet("background-color:transparent;border:0;")

        self.hCRpushButtonBlue = QtWidgets.QPushButton(self.hCRBgroupBox)
        self.hCRpushButtonBlue.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.hCRpushButtonBlue.setStyleSheet("background-color: rgb(0, 170, 255);border-radius: 15px;\n"
"")
        self.hCRpushButtonBlue.setText("")
        self.hCRpushButtonBlue.setObjectName("hCRpushButtonBlue")
        self.hCRpushButtonWhite = QtWidgets.QPushButton(self.hCRBgroupBox)
        self.hCRpushButtonWhite.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.hCRpushButtonWhite.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.hCRpushButtonWhite.setText("")
        self.hCRpushButtonWhite.setObjectName("hCRpushButtonWhite")
        self.hCRpushButtonBlueYellow = QtWidgets.QPushButton(self.hCRBgroupBox)
        self.hCRpushButtonBlueYellow.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.hCRpushButtonBlueYellow.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border-radius: 15px;")
        self.hCRpushButtonBlueYellow.setText("")
        self.hCRpushButtonBlueYellow.setObjectName("hCRpushButtonBlueYellow")
        self.hCRpushButtonGreen = QtWidgets.QPushButton(self.hCRBgroupBox)
        self.hCRpushButtonGreen.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.hCRpushButtonGreen.setAutoFillBackground(False)
        self.hCRpushButtonGreen.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"alternate-background-color: rgb(0, 170, 0);\n"
"border-radius: 15px;")
        self.hCRpushButtonGreen.setText("")
        self.hCRpushButtonGreen.setObjectName("hCRpushButtonGreen")

        # ------------------------------------------------------------
        # Цвет рамок для остальных объектов
        # ------------------------------------------------------------
        self.oCRBgroupBox_2 = QtWidgets.QGroupBox(Form)
        self.oCRBgroupBox_2.setGeometry(QtCore.QRect(50, 330, 281, 71))
        self.oCRBgroupBox_2.setTitle("")
        self.oCRBgroupBox_2.setObjectName("oCRBgroupBox_2")
        self.oCRBgroupBox_2.setStyleSheet("background-color:transparent;border:0;")

        self.oCRBpushButtonGreen = QtWidgets.QPushButton(self.oCRBgroupBox_2)
        self.oCRBpushButtonGreen.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.oCRBpushButtonGreen.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"border-radius: 15px;")
        self.oCRBpushButtonGreen.setText("")
        self.oCRBpushButtonGreen.setObjectName("oCRBpushButtonGreen")
        self.oCRBpushButtonBlue = QtWidgets.QPushButton(self.oCRBgroupBox_2)
        self.oCRBpushButtonBlue.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.oCRBpushButtonBlue.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"border-radius: 15px;")
        self.oCRBpushButtonBlue.setText("")
        self.oCRBpushButtonBlue.setObjectName("oCRBpushButtonBlue")
        self.oCRBpushButtonWhite = QtWidgets.QPushButton(self.oCRBgroupBox_2)
        self.oCRBpushButtonWhite.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.oCRBpushButtonWhite.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.oCRBpushButtonWhite.setText("")
        self.oCRBpushButtonWhite.setObjectName("oCRBpushButtonWhite")
        self.oCRBpushButtonYellow = QtWidgets.QPushButton(self.oCRBgroupBox_2)
        self.oCRBpushButtonYellow.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.oCRBpushButtonYellow.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border-radius: 15px;")
        self.oCRBpushButtonYellow.setText("")
        self.oCRBpushButtonYellow.setObjectName("oCRBpushButtonYellow")

        # ------------------------------------------------------------
        # Толщина рамок
        # ------------------------------------------------------------
        self.ThickFramegroupBox_5 = QtWidgets.QGroupBox(Form)
        self.ThickFramegroupBox_5.setGeometry(QtCore.QRect(580, 470, 291, 71))
        self.ThickFramegroupBox_5.setTitle("")
        self.ThickFramegroupBox_5.setObjectName("ThickFramegroupBox_5")
        self.ThickFramegroupBox_5.setStyleSheet("background-color:transparent;border:0;")

        self.ThickFramepushButton_1 = QtWidgets.QPushButton(self.ThickFramegroupBox_5)
        self.ThickFramepushButton_1.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.ThickFramepushButton_1.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(101, 127, 140, 1);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.ThickFramepushButton_1.setObjectName("ThickFramepushButton_1")
        self.ThickFramepushButton_2 = QtWidgets.QPushButton(self.ThickFramegroupBox_5)
        self.ThickFramepushButton_2.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.ThickFramepushButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"border-radius: 15px;")
        self.ThickFramepushButton_2.setObjectName("ThickFramepushButton_2")
        self.ThickFramepushButton_3 = QtWidgets.QPushButton(self.ThickFramegroupBox_5)
        self.ThickFramepushButton_3.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.ThickFramepushButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"border-radius: 15px;")
        self.ThickFramepushButton_3.setObjectName("ThickFramepushButton_3")
        self.ThickFramepushButton_4 = QtWidgets.QPushButton(self.ThickFramegroupBox_5)
        self.ThickFramepushButton_4.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.ThickFramepushButton_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.ThickFramepushButton_4.setObjectName("ThickFramepushButton_4")


        self.mCFRBgroupBox_3 = QtWidgets.QGroupBox(Form)
        self.mCFRBgroupBox_3.setGeometry(QtCore.QRect(50, 460, 281, 71))
        self.mCFRBgroupBox_3.setTitle("")
        self.mCFRBgroupBox_3.setObjectName("mCFRBgroupBox_3")
        self.mCFRBgroupBox_3.setStyleSheet("background-color:transparent;border:0;")

        # ------------------------------------------------------------
        # Цвет рамок для границ
        # ------------------------------------------------------------
        self.CFB_RBgroupBox_4 = QtWidgets.QGroupBox(Form)
        self.CFB_RBgroupBox_4.setGeometry(QtCore.QRect(50, 580, 281, 71))
        self.CFB_RBgroupBox_4.setTitle("")
        self.CFB_RBgroupBox_4.setObjectName("CFB_RBgroupBox_4")
        self.CFB_RBgroupBox_4.setStyleSheet("background-color:transparent;border:0;")

        self.CFB_RBpushButtonGreen_2 = QtWidgets.QPushButton(self.mCFRBgroupBox_3)
        self.CFB_RBpushButtonGreen_2.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.CFB_RBpushButtonGreen_2.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"border-radius: 15px;")
        self.CFB_RBpushButtonGreen_2.setText("")
        self.CFB_RBpushButtonGreen_2.setObjectName("CFB_RBpushButtonGreen_2")
        self.CFB_RBpushButtonBlue_2 = QtWidgets.QPushButton(self.mCFRBgroupBox_3)
        self.CFB_RBpushButtonBlue_2.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.CFB_RBpushButtonBlue_2.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"border-radius: 15px;")
        self.CFB_RBpushButtonBlue_2.setText("")
        self.CFB_RBpushButtonBlue_2.setObjectName("CFB_RBpushButtonBlue_2")
        self.CFB_RBpushButtonWhite_2 = QtWidgets.QPushButton(self.mCFRBgroupBox_3)
        self.CFB_RBpushButtonWhite_2.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.CFB_RBpushButtonWhite_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.CFB_RBpushButtonWhite_2.setText("")
        self.CFB_RBpushButtonWhite_2.setObjectName("CFB_RBpushButtonWhite_2")
        self.CFB_RBpushButtonYellow_2 = QtWidgets.QPushButton(self.mCFRBgroupBox_3)
        self.CFB_RBpushButtonYellow_2.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.CFB_RBpushButtonYellow_2.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border-radius: 15px;")
        self.CFB_RBpushButtonYellow_2.setText("")
        self.CFB_RBpushButtonYellow_2.setObjectName("CFB_RBpushButtonYellow_2")



        self.mCFRpushButtonGreen_3 = QtWidgets.QPushButton(self.CFB_RBgroupBox_4)
        self.mCFRpushButtonGreen_3.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.mCFRpushButtonGreen_3.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"border-radius: 15px;")
        self.mCFRpushButtonGreen_3.setText("")
        self.mCFRpushButtonGreen_3.setObjectName("mCFRpushButtonGreen_3")
        self.mCFRpushButtonBlue_3 = QtWidgets.QPushButton(self.CFB_RBgroupBox_4)
        self.mCFRpushButtonBlue_3.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.mCFRpushButtonBlue_3.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"border-radius: 15px;")
        self.mCFRpushButtonBlue_3.setText("")
        self.mCFRpushButtonBlue_3.setObjectName("mCFRpushButtonBlue_3")
        self.mCFRpushButtonWhite_3 = QtWidgets.QPushButton(self.CFB_RBgroupBox_4)
        self.mCFRpushButtonWhite_3.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.mCFRpushButtonWhite_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.mCFRpushButtonWhite_3.setText("")
        self.mCFRpushButtonWhite_3.setObjectName("mCFRpushButtonWhite_3")
        self.mCFRpushButtonYellow_3 = QtWidgets.QPushButton(self.CFB_RBgroupBox_4)
        self.mCFRpushButtonYellow_3.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.mCFRpushButtonYellow_3.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border-radius: 15px;")
        self.mCFRpushButtonYellow_3.setText("")
        self.mCFRpushButtonYellow_3.setObjectName("mCFRpushButtonYellow_3")

        # ------------------------------------------------------------
        # Толщина границ
        # ------------------------------------------------------------
        self.ThickBordergroupBox_6 = QtWidgets.QGroupBox(Form)
        self.ThickBordergroupBox_6.setGeometry(QtCore.QRect(580, 580, 291, 71))
        self.ThickBordergroupBox_6.setTitle("")
        self.ThickBordergroupBox_6.setObjectName("ThickBordergroupBox_6")
        self.ThickBordergroupBox_6.setStyleSheet("background-color:transparent;border:0;")

        self.ThickBorderpushButton_1 = QtWidgets.QPushButton(self.ThickBordergroupBox_6)
        self.ThickBorderpushButton_1.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.ThickBorderpushButton_1.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(101, 127, 140, 1);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.ThickBorderpushButton_1.setObjectName("ThickBorderpushButton_1")
        self.ThickBorderpushButton_2 = QtWidgets.QPushButton(self.ThickBordergroupBox_6)
        self.ThickBorderpushButton_2.setGeometry(QtCore.QRect(80, 10, 51, 51))
        self.ThickBorderpushButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"border-radius: 15px;")
        self.ThickBorderpushButton_2.setObjectName("ThickBorderpushButton_2")
        self.ThickBorderpushButton_3 = QtWidgets.QPushButton(self.ThickBordergroupBox_6)
        self.ThickBorderpushButton_3.setGeometry(QtCore.QRect(150, 10, 51, 51))
        self.ThickBorderpushButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"border-radius: 15px;")
        self.ThickBorderpushButton_3.setObjectName("ThickBorderpushButton_3")
        self.ThickBorderpushButton_4 = QtWidgets.QPushButton(self.ThickBordergroupBox_6)
        self.ThickBorderpushButton_4.setGeometry(QtCore.QRect(220, 10, 51, 51))
        self.ThickBorderpushButton_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgba(101, 127, 140, 1);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.ThickBorderpushButton_4.setObjectName("ThickBorderpushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ThickFramepushButton_1.setText(_translate("Form", "1"))
        self.ThickFramepushButton_2.setText(_translate("Form", "2"))
        self.ThickFramepushButton_3.setText(_translate("Form", "3"))
        self.ThickFramepushButton_4.setText(_translate("Form", "4"))
        self.ThickBorderpushButton_1.setText(_translate("Form", "1"))
        self.ThickBorderpushButton_2.setText(_translate("Form", "2"))
        self.ThickBorderpushButton_3.setText(_translate("Form", "3"))
        self.ThickBorderpushButton_4.setText(_translate("Form", "4"))



import xz_rc
