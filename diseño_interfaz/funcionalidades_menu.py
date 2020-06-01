from menu import *
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.analizar_bbdd.setEnabled(False)
        self.log.setEnabled(False)
        self.encontrar_root.clicked.connect(self.boton_encontrar)
        self.rootear.clicked.connect(self.boton_root)
        self.multimedia.clicked.connect(self.boton_multimedia)
        self.base_datos.clicked.connect(self.boton_base_datos)
        self.analizar_bbdd.clicked.connect(self.boton_analizar_bbdd)
        self.log.clicked.connect(self.boton_log)
       # las funciones no deben tener el mismo nombre que el elemento 
      
    def boton_encontrar(self):
        self.encontrar_root.setStyleSheet("background-color: red")
    
    def boton_root(self):
        self.rootear.setStyleSheet("background-color: red")
    
    def boton_multimedia(self):
        self.multimedia.setStyleSheet("background-color: red")
    
    def boton_base_datos(self):
        self.base_datos.setStyleSheet("background-color: red")
    
    def boton_analizar_bbdd(self):
        self.analizar_bbdd.setStyleSheet("background-color: red")
    
    def boton_log(self):
        self.log.setStyleSheet("background-color: red")
    

    


   

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()