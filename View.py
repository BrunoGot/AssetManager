'''import sys
import os
from os.path import basename

from PySide2 import QtCore, QtGui, QtWidgets
import file_system as fs
import View.AnimButton as animBut


class MyWidget( QtWidgets.QWidget):
    lines =4
    row = 4
    index = 0
    current_asset = ""
    asset_views = {}

    def __init__(self):

        #datas
        self.file_system = fs.file_system()
        self.file_system.parse_asset_list()
        self.assets = self.file_system.get_assets() #get the list of all assets to display

        #GUI
        QtWidgets.QWidget.__init__(self)

        lib_layout = self.lib_view() #crea  te the library view

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(lib_layout)

        self.setLayout(main_layout)


    def change_view(self, asset):
        print("change_view asset type : "+str(type(asset)))
        self.current_asset=asset
        #self.index = (self.index+1)%2
        #self.asset_stack_layout.setLayout()
        self.asset_views[self.current_asset.name] = asset_view(self)
        view = self.asset_views[self.current_asset.name]
        view.set_datas(self.current_asset)
        #self.asset_view.get_view().widget().show()
        view.show()
        #self.stack.setCurrentIndex(1)


    #def show_all_assets(self):
    #    self.stack.setCurrentIndex(0)

    def lib_view(self):
        frame_layout = self.display_assets()

        self.scroll_layout = QtWidgets.QScrollArea(self)
        self.scroll_layout.setWidget(frame_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.scroll_layout)
        return main_layout

        """def asset_view(self):
        asset_name = self.current_asset
        self.label = QtWidgets.QLabel(asset_name)
        icon = QtGui.QPixmap('add.jpg')
        button = QtWidgets.QPushButton()
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(256, 256))
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(button)
        main_layout.addWidget(self.label)
        return main_layout"""

    def display_assets(self):
        print(f"assetslib = {self.assets}")
        nb_assets = len(self.assets)
        row = 4
        print(nb_assets)
        lines = int(round(nb_assets/row))
        print("lines = "+str(lines))
        assets_layout = QtWidgets.QHBoxLayout()
        index = 0
        for x in range(0, row):
            vert_layout = QtWidgets.QVBoxLayout()
            for y in range(0, round(lines)):
                print("assets.keys() ="+str())
                if(index<len(list(self.assets))):
                    asset_button = self.create_asset_button(list(self.assets)[index])
                    vert_layout.addLayout(asset_button)
                    assets_layout.addLayout(vert_layout)
                index += 1

        frame_layout = QtWidgets.QWidget()
        frame_layout.setLayout(assets_layout)
        return frame_layout

    def create_asset_button(self, asset_name):
        asset = self.assets[asset_name]
        thumbnail = asset.thumbnail()
        print("##thumbnail = "+thumbnail)
        if not thumbnail:
            thumbnail = 'add.jpg'
        icon = QtGui.QPixmap(thumbnail)
        button = QtWidgets.QPushButton()
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(256, 256))
        #print("create_asset_button :: asset tasks = "+str(asset.tasks))
        #print("type asset = "+str(type(asset)))
        button.clicked.connect(lambda b=True, a= asset : self.change_view(a))
        text = QtWidgets.QLabel(asset_name)
        b_layout = QtWidgets.QVBoxLayout()
        b_layout.addWidget(button)
        b_layout.addWidget(text)
        return b_layout

class asset_view(QtWidgets.QWidget):

    def __init__(self, main_class):
        self.task_buttons = []  # array containing the tasks button
        self.subtask_buttons = []  # array containing the subtasks button

        QtWidgets.QWidget.__init__(self)

        #setting the GUI there
        self.main_layout = QtWidgets.QVBoxLayout()
        self.h_layout = QtWidgets.QHBoxLayout()
        self.info_layout = QtWidgets.QVBoxLayout()
        self.label_type = QtWidgets.QLabel()
        self.label_total_size = QtWidgets.QLabel()

        #self.info_layout.addWidget(self.label_title)
        self.info_layout.addWidget(self.label_type)
        self.info_layout.addWidget(self.label_total_size)
        #handle version layout
        self.version_dropdown = QtWidgets.QComboBox()
        self.version_dropdown.activated[str].connect(self.select_version)
        #handle tasks & subtask layout
        self.task_layout = QtWidgets.QHBoxLayout()
        self.tasks_groupbox = QtWidgets.QGroupBox("Tasks")
        self.v_task_layout = QtWidgets.QVBoxLayout()
        self.v_task_layout.addLayout(self.task_layout)
        self.tasks_groupbox.setLayout(self.v_task_layout)

        #layout to set version and subtasks
        self.subtasks_groupbox = QtWidgets.QGroupBox("Subtasks")
        self.subtask_layout = QtWidgets.QHBoxLayout()
        self.v_subtask_layout = QtWidgets.QVBoxLayout()
        self.v_subtask_layout.addLayout(self.subtask_layout)
        self.v_subtask_layout.addWidget(QtWidgets.QLabel("Version : "))
        self.v_subtask_layout.addWidget(self.version_dropdown)
        self.subtasks_groupbox.setLayout(self.v_subtask_layout)

        self.v_task_layout.addWidget(self.subtasks_groupbox)

        self.info_layout.addWidget(self.tasks_groupbox)

        #horizontal layer to open asset and folder
        self.open_asset_button = QtWidgets.QPushButton("open file")
        self.open_folder_button = QtWidgets.QPushButton("open folder")
        self.open_folder_button.clicked.connect(self.open_folder)
        self.h_layout_open_buttons = QtWidgets.QHBoxLayout()
        self.h_layout_open_buttons.addWidget(self.open_asset_button)
        self.h_layout_open_buttons.addWidget(self.open_folder_button)
        self.info_layout.addLayout(self.h_layout_open_buttons)

        self.h_layout.addLayout(self.info_layout)

        #button viewer widget
        self.viewer_tab = QtWidgets.QTabWidget()
        self.flip_button = animBut.AnimButton() #QtWidgets.QPushButton()
        self.render_button = animBut.AnimButton() #QtWidgets.QPushButton()
        #thumbnail = self.asset.thumbnail()
        #if not thumbnail:
        thumbnail = 'add.jpg'
        self.icon = QtGui.QPixmap(thumbnail)
        icon_size = QtCore.QSize(384,384)
        self.flip_button = self.set_viewer_button(self.flip_button, self.icon, icon_size)
        self.render_button = self.set_viewer_button(self.render_button, self.icon, icon_size)
        self.h_layout.addWidget(self.viewer_tab)
        self.viewer_tab.addTab(self.flip_button, "Flip")
        self.viewer_tab.addTab(self.render_button, "Render")
        #self.main_layout.addWidget(self.viewerTab)
        #self.h_layout.addWidget()

        #top layout
        self.h_layout_top = QtWidgets.QHBoxLayout()
        self.label_title = QtWidgets.QLabel("test")
        #self.return_button = QtWidgets.QPushButton("return")
        #self.return_button.clicked.connect(main_class.show_all_assets)
#        self.h_layout_top.addWidget(self.return_button)
        self.h_layout_top.addWidget(self.label_title)
        self.main_layout.addLayout(self.h_layout_top)
        self.main_layout.addLayout(self.h_layout)
        self.setLayout(self.main_layout)

    def set_viewer_button(self, annim_button, icon, icon_size):
        annim_button.setIcon(icon)
        annim_button.setIconSize(icon_size)
        return annim_button

    def set_datas(self, asset):
        self.setWindowTitle(asset.name)
        """this function is loading datas of the asset in the GUI"""
        self.asset = asset
        self.label_title.setText(asset.name)
        self.label_type.setText("Type : "+asset.type)
        size = asset.total_size/(1024*1024)
        size = round(size,2)
        print("size  = "+str(size) )
        self.label_total_size.setText("Total size : "+f"{size:,}")
        for i in asset.tasks:
            print(i)
            task_button = self.create_task_button(i)
            #task_button.click()
            self.task_layout.addWidget(task_button)
            self.task_buttons.append(task_button)
        #let's check the first button by default. By clicking the task buttons, the subtask are generated also
        self.task_buttons[0].click()
        #update the version according to the selected task & subtask
        self.refresh_versions()
        #update the thumbnail according to the selecte version

        #update the flip& render frames
        fpath = asset.CurrentFlipDir() #return the path of the flip directory for  the current task/subtask/work
        rpath = asset.current_render_dir()
        self.update_buttons_viewer(fpath, rpath)

    def update_buttons_viewer(self, fpath, rpath):
        # update the flip frames
        self.load_frames_for_viewer(self.flip_button, fpath)
        # update render frames
        self.load_frames_for_viewer(self.render_button, rpath)

    def load_frames_for_viewer(self, anim_button, frame_path):
        """check if the folder is correct and load the frames for the anim buttons"""
        frames = []
        if os.path.exists(frame_path):
            frames = os.listdir(frame_path)
            #anim_button.setFrames(basePath=frame_path, frames=frames)
        #look for some thumbnail in some fallback folder if no render or flipbook exist
        if len(frames) == 0 and os.path.exists(self.asset.get_current_version_path()):
            frames = os.listdir(self.asset.get_current_version_path())
        print(f"current version = {self.asset.get_current_version_path()}, frames = {len(frames)}")
        anim_button.setFrames(basePath=frame_path, frames=frames)


    def populate_dropdown_version(self,versions):
        for v in versions:
            self.version_dropdown.addItem(v)
        #by default set to the last version
        index = len(versions)-1
        self.version_dropdown.setCurrentIndex(index)
        print("index = " + str(index))
        print("versions = "+str(versions))
        print("versions[index] = "+list(versions)[index])
        self.asset.set_current_version(list(versions)[index])

    def get_view(self): #return the layout to be integred in the panel
        return self.main_layout

    def open_asset(self):
        print("open asset")

    def create_task_button(self, name):
        button = QtWidgets.QPushButton(name)
        button.setCheckable(True)
        button.clicked.connect(lambda b=True, t=button: self.select_task(t))
        return button
        #QtWidgets.

    def create_subtask_button(self, name):
        button = QtWidgets.QPushButton(name)
        button.setCheckable(True)
        button.clicked.connect(lambda b=True, t=button: self.select_subtask(t))
        return button

    def select_task(self, selected_button):
        nb = self.task_layout.count()
        print("clicked on : "+selected_button.text())
        for i in range(0,nb):
            button = self.task_layout.itemAt(i).widget()
            if(button.text() != selected_button.text()):
                button.setChecked(False)
        #self.subtask_layout = QtWidgets.QHBoxLayout()
        self.asset.set_current_task(selected_button.text())
        self.refresh_subtask(selected_button.text())
            #button.widget().text()

            #print(button.widget().text())
        #print()

    def refresh_subtask(self, selected_task):
        """refresh the subtask button list on the gui"""
        print("refresh subtasks for "+selected_task)
        self.subtask_buttons.clear()
        #self.subtask_layout.remove
        #todo :
        #for all widget, removethem. Then remove also verion options
        #print("self.subtask_layout.count() = "+str(self.subtask_layout.count()))
        for i in reversed(range(0, self.subtask_layout.count())):
            print("remove")
            self.subtask_layout.itemAt(i).widget().setParent(None)

        for i in self.asset.get_subtasks(selected_task).keys():
            subtask_button = self.create_subtask_button(i)
            self.subtask_layout.addWidget(subtask_button)
            print("subtasks = " + i)
            self.subtask_buttons.append(subtask_button)

        self.subtask_buttons[0].click() #setChecked(True)

    def refresh_versions(self):
        for i in reversed(range(self.version_dropdown.count())):
            self.version_dropdown.removeItem(i)
        versions = self.asset.get_current_versions()
        self.populate_dropdown_version(versions)

    def select_subtask(self, selected_button):
        current_subtask = self.asset.current_subtask()
        if(current_subtask!= None):
            if(current_subtask.name()!=selected_button.text()):
                nb = len(self.subtask_buttons)
                for i in range(0, nb):
                    button = self.subtask_layout.itemAt(i).widget()
                    if (button.text() != selected_button.text()):
                        button.setChecked(False)
        self.asset.set_current_subtask(selected_button.text())
        self.refresh_versions()

    def select_version(self, version):
        print("version selected = "+version)
        self.asset.set_current_version(version)
        fpath = self.asset.CurrentFlipDir() #return the path of the flip directory for  the current task/subtask/work
        rpath = self.asset.current_render_dir()
        self.update_buttons_viewer(fpath, rpath)


    def open_folder(self):
        self.asset.open_folder()

def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()'''