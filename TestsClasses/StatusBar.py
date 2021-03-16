import sys
from PySide2 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage("ready")
        self.setGeometry(300,300,250,150)
        self.setWindowTitle('StatusBar')
        self.show()

def main():
    app=QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()