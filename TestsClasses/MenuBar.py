import sys
from PySide2 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        exitAction = QtWidgets.QAction(QtGui.QIcon("exit.png"), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Menubar')
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

