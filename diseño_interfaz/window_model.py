# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\window_model.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Window_model(object):
    def setupUi(self, Window_model):
        Window_model.setObjectName("Window_model")
        Window_model.resize(400, 150)
        self.centralwidget = QtWidgets.QWidget(Window_model)
        self.centralwidget.setObjectName("centralwidget")
        self.lblText = QtWidgets.QLabel(self.centralwidget)
        self.lblText.setGeometry(QtCore.QRect(30, 20, 341, 101))
        self.lblText.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblText.setObjectName("lblText")
        Window_model.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_model)
        QtCore.QMetaObject.connectSlotsByName(Window_model)

    def retranslateUi(self, Window_model):
        _translate = QtCore.QCoreApplication.translate
        Window_model.setWindowTitle(_translate("Window_model", "MainWindow"))
        self.lblText.setText(_translate("Window_model", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window_model = QtWidgets.QMainWindow()
    ui = Ui_Window_model()
    ui.setupUi(Window_model)
    Window_model.show()
    sys.exit(app.exec_())

