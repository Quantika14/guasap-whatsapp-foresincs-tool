import sys, time

from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication


class waitWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info")
        self.resize(600,200)
        self.VLayout = QtWidgets.QVBoxLayout(self)
        self.message = QtWidgets.QLabel(self)
        self.message.setFixedWidth(550)
        self.message.setText("Please wait while input file is being read")
        self.VLayout.addWidget(self.message)
        self.show()

    def closeWindow(self):
        self.close()

app = QApplication(sys.argv)
w = waitWindow()
w.exec_()
w.closeWindow()