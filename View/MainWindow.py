import sys
from PySide2 import QtWidgets, QtGui
import View
import config_view
import file_system as fs

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_system = fs.file_system()
        self.initUI()

    def initUI(self):
        # Menu bar
        menubar = self.menuBar()
        ## Define actions
        exitAction = QtWidgets.QAction(QtGui.QIcon("exit.png"), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.close)
        #
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
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.addTab(self.default_lib,self.file_system.default_config_name)

        self.setCentralWidget(self.tab_widget)

        #self.setGeometry(300,300,250,150)
        self.setWindowTitle('Asset Manager')
        self.show()

    def open_config_menu(self):
        self.config_window = config_view.ConfigView(self)
        self.config_window.show()

    def add_new_config(self, config_name):
        print("load config : "+config_name)
        self.tab_widget.addTab(View.LibraryView(config_name), config_name)

    def on_tab_changed(self,index):
        self.file_system.set_current_config_index(index)

def GUI_Style(app):
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