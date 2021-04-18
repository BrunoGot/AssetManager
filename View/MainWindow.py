import sys
from PySide2 import QtWidgets, QtGui
import View
import ConfigView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        # Menu bar
        menubar = self.menuBar()
        ## Define actions
        exitAction = QtWidgets.QAction(QtGui.QIcon("exit.png"), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.close)
        #-
        option_action = QtWidgets.QAction(QtGui.QIcon("exit.png"), '&Options', self)
        option_action.setShortcut('Ctrl+O')
        option_action.setStatusTip("Options")
        option_action.triggered.connect(self.open_config_menu)
        ##add it to the menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(option_action)

        #status bar
        self.statusBar()

        self.default_lib = View.LibraryView()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.default_lib,"default")

        self.setCentralWidget(self.tab_widget)

        #self.setGeometry(300,300,250,150)
        self.setWindowTitle('Asset Manager')
        self.show()

    def open_config_menu(self):
        self.config_window = ConfigView.MainView()
        self.config_window.show()

def GUI_Style( app):
    file_qss = open("Styles/Combinear.qss")
    with file_qss:
        qss = file_qss.read()
        #print("QSS = "+qss)
        app.setStyleSheet(qss)

def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI_Style(app)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()