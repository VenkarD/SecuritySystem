# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1002, 671)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(":root {\n"
"    padding: 0px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"#centralwidget {\n"
"    border-image: url(:/everything/resources/bk.jpg) 0 0 0 0 stretch stretch;\n"
"    background: red;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_bar = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_bar.sizePolicy().hasHeightForWidth())
        self.top_bar.setSizePolicy(sizePolicy)
        self.top_bar.setMinimumSize(QtCore.QSize(0, 66))
        self.top_bar.setStyleSheet("background: #F0F8FD")
        self.top_bar.setObjectName("top_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_bar)
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.top_bar)
        self.widget.setMinimumSize(QtCore.QSize(152, 0))
        self.widget.setMaximumSize(QtCore.QSize(152, 52))
        self.widget.setStyleSheet("background-image: url(:/everything/resources/logo.png);")
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.log_btn = QtWidgets.QPushButton(self.top_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_btn.sizePolicy().hasHeightForWidth())
        self.log_btn.setSizePolicy(sizePolicy)
        self.log_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.log_btn.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.log_btn.setAcceptDrops(False)
        self.log_btn.setToolTipDuration(-1)
        self.log_btn.setStyleSheet("background-image: url(:/everything/resources/buttonBK.jpg);\n"
"font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.log_btn.setAutoDefault(False)
        self.log_btn.setObjectName("log_btn")
        self.horizontalLayout.addWidget(self.log_btn)
        self.refresh_btn = QtWidgets.QPushButton(self.top_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_btn.sizePolicy().hasHeightForWidth())
        self.refresh_btn.setSizePolicy(sizePolicy)
        self.refresh_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.refresh_btn.setStyleSheet("background-image: url(:/everything/resources/buttonBK.jpg);\n"
"font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.refresh_btn.setObjectName("refresh_btn")
        self.horizontalLayout.addWidget(self.refresh_btn)
        self.settings_btn = QtWidgets.QPushButton(self.top_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_btn.sizePolicy().hasHeightForWidth())
        self.settings_btn.setSizePolicy(sizePolicy)
        self.settings_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.settings_btn.setBaseSize(QtCore.QSize(0, 0))
        self.settings_btn.setStyleSheet("background-image: url(:/everything/resources/buttonBK.jpg);\n"
"font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.settings_btn.setObjectName("settings_btn")
        self.horizontalLayout.addWidget(self.settings_btn)
        self.exit_btn = QtWidgets.QPushButton(self.top_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_btn.sizePolicy().hasHeightForWidth())
        self.exit_btn.setSizePolicy(sizePolicy)
        self.exit_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.exit_btn.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(:/everything/resources/buttonBK.jpg);")
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        self.verticalLayout.addWidget(self.top_bar)
        self.main_grid = QtWidgets.QGridLayout()
        self.main_grid.setObjectName("main_grid")
        self.verticalLayout.addLayout(self.main_grid)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.log_btn.setText(_translate("MainWindow", "Лог оператора"))
        self.refresh_btn.setText(_translate("MainWindow", "Обновить"))
        self.settings_btn.setText(_translate("MainWindow", "Настройки"))
        self.exit_btn.setText(_translate("MainWindow", "Выход"))

import xz_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

