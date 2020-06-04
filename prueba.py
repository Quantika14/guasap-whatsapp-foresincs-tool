import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot

class Popup(QWidget):
	def __init__(self, parent=None, texto = ""):
		super().__init__(self)
		self.texto = texto
		self.setWindowTitle("My Own Title")
		self.setGeometry(100, 100, 640, 480)

		self.label = QLabel(self.texto, self)
		self.label.adjustSize()

		hbox=QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.label)

		vbox=QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Popup('hola')
    sys.exit(app.exec_())