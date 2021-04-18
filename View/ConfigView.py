#windows to edit the configuration file
import file_system as fs
from PySide2 import QtCore, QtGui, QtWidgets

class MainView(QtWidgets.QWidget):
    def __init__(self):

        #GUI
        QtWidgets.QWidget.__init__(self)
        self.file_system = fs.file_system()
        self.init_GUI()
        self.set_default_values()


    def init_GUI(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.configuration_file_label = QtWidgets.QLabel("Configuration File")
        self.main_layout.addWidget(self.configuration_file_label)
        self.description_label = QtWidgets.QLabel("Configure here the template of your pipeline")
        self.main_layout.addWidget(self.description_label)
        #button to import configuration file
        self.import_button = QtWidgets.QPushButton()
        self.import_button.setText("Import")
        self.main_layout.addWidget(self.import_button)

        #namle of the configuration
        self.config_name_layout = QtWidgets.QHBoxLayout()
        self.config_name_label = QtWidgets.QLabel("Config Name : ")
        self.config_name_input = QtWidgets.QLineEdit()
        self.config_name_layout.addWidget(self.config_name_label)
        self.config_name_layout.addWidget(self.config_name_input)
        self.main_layout.addLayout(self.config_name_layout)

        #Asset File Name : name of the file
        self.asset_file_name_layout = QtWidgets.QHBoxLayout()
        self.asset_file_name_label = QtWidgets.QLabel("File Name Template: ")
        self.asset_file_name_input = QtWidgets.QLineEdit()
        self.asset_file_name_layout.addWidget(self.asset_file_name_label)
        self.asset_file_name_layout.addWidget(self.asset_file_name_input)
        self.main_layout.addLayout(self.asset_file_name_layout)

        # Project path
        self.project_layout = QtWidgets.QHBoxLayout()
        self.project_label = QtWidgets.QLabel("project : ")
        self.project_input = QtWidgets.QLineEdit()
        self.project_layout.addWidget(self.project_label)
        self.project_layout.addWidget(self.project_input)
        self.main_layout.addLayout(self.project_layout)

        # Asset Path
        self.asset_path_layout = QtWidgets.QHBoxLayout()
        self.asset_path_label = QtWidgets.QLabel("Asset : ")
        self.asset_path_input = QtWidgets.QLineEdit()
        self.asset_path_layout.addWidget(self.asset_path_label)
        self.asset_path_layout.addWidget(self.asset_path_input)
        self.main_layout.addLayout(self.asset_path_layout)

        #Path of the file in the asset folder
        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel("Asset File Path : ")
        self.file_input = QtWidgets.QLineEdit()
        self.file_layout.addWidget(self.file_label)
        self.file_layout.addWidget(self.file_input)
        self.main_layout.addLayout(self.file_layout)

        #Path for the worksapce
        self.workspace_layout = QtWidgets.QHBoxLayout()
        self.workspace_label = QtWidgets.QLabel("Workspace : ")
        self.workspace_input = QtWidgets.QLineEdit()
        self.workspace_layout.addWidget(self.workspace_label)
        self.workspace_layout.addWidget(self.workspace_input)
        self.main_layout.addLayout(self.workspace_layout)

        # Path for the Render folder
        self.render_layout = QtWidgets.QHBoxLayout()
        self.render_label = QtWidgets.QLabel("Render : ")
        self.render_input = QtWidgets.QLineEdit()
        self.render_layout.addWidget(self.render_label)
        self.render_layout.addWidget(self.render_input)
        self.main_layout.addLayout(self.render_layout)

        # Path for the Cache folder
        self.cache_layout = QtWidgets.QHBoxLayout()
        self.cache_label = QtWidgets.QLabel("Cache : ")
        self.cache_input = QtWidgets.QLineEdit()
        self.cache_layout.addWidget(self.cache_label)
        self.cache_layout.addWidget(self.cache_input)
        self.main_layout.addLayout(self.cache_layout)

        # Path for the Cache folder
        self.texture_layout = QtWidgets.QHBoxLayout()
        self.texture_label = QtWidgets.QLabel("Textures : ")
        self.texture_input = QtWidgets.QLineEdit()
        self.texture_layout.addWidget(self.texture_label)
        self.texture_layout.addWidget(self.texture_input)
        self.main_layout.addLayout(self.texture_layout)

        # Path for the Flip books folder
        self.flip_layout = QtWidgets.QHBoxLayout()
        self.flip_label = QtWidgets.QLabel("Flips : ")
        self.flip_input = QtWidgets.QLineEdit()
        self.flip_layout.addWidget(self.flip_label)
        self.flip_layout.addWidget(self.flip_input)
        self.main_layout.addLayout(self.flip_layout)

        self.bottom_buttons_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save")
        self.bottom_buttons_layout.addWidget(self.save_button)
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setText("Export")
        self.bottom_buttons_layout.addWidget(self.export_button)
        self.main_layout.addLayout(self.bottom_buttons_layout)
        self.setLayout(self.main_layout)

    def set_default_values(self):
        """parse the file, foreach line, assign the value to the right parameter"""
        config = self.file_system.get_config_file()
        print(config.asset_path.pattern)

        self.project_input.setText(config.project_directory.pattern)
        self.asset_file_name_input.setText(config.asset_file_name.pattern)
        self.asset_path_input.setText(config.asset_path.pattern)

