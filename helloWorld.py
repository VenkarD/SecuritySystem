from PyQt5 import QtCore, QtGui
import sys

app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
window.setWindowTitle("Изображение в качестве фона")
window.resize(300, 200)

# создание объекта-палитры с помощью получения текущей палитры компонента
pal = window.palette()
# установка цвета (3) для фона (2) состояния Normal (1)
pal.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Background,
             QtGui.QBrush(QtGui.QPixmap("green.png")))
window.setPalette(pal)  # использование объекта-палитры

label = QtGui.QLabel("Hello World!")
pal1 = label.palette()
pal1.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Background,
              QtGui.QBrush(QtGui.QPixmap("blue.png")))
label.setPalette(pal1)
label.setAlignment(QtCore.Qt.AlignCenter)
label.setStyleSheet("color: #ffffff; font-family: Times; font-size: 18px;")
label.setAutoFillBackground(True)

label2 = QtGui.QLabel("Goodbye World!")
label2.setAlignment(QtCore.Qt.AlignCenter)
label2.setStyleSheet('background-image: url("yellow.png"); font-family: Times; font-size: 18px;')

vbox = QtGui.QVBoxLayout()
vbox.addWidget(label)
vbox.addWidget(label2)
window.setLayout(vbox)

window.show()
sys.exit(app.exec_())