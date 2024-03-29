#windows to edit the configuration file
import os
import file_system as fs
from PySide2 import QtCore, QtGui, QtWidgets

class MainView(QtWidgets.QWidget):
    def __init__(self, main_window):
        #GUI
        QtWidgets.QWidget.__init__(self)
        self.file_system = fs.file_system()
        self.init_GUI()
        self.set_default_values()
        self.main_window = main_window

    def init_GUI(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.configuration_file_label = QtWidgets.QLabel("Configurations File")
        self.main_layout.addWidget(self.configuration_file_label)
        self.description_label = QtWidgets.QLabel("Configure here the template of your pipeline")
        self.main_layout.addWidget(self.description_label)
        #button to import configuration file
        self.import_button = QtWidgets.QPushButton()
        self.import_button.setText("Import")
        self.main_layout.addWidget(self.import_button)

        #name of the configuration
        self.config_name_layout = QtWidgets.QHBoxLayout()
        self.config_name_label = QtWidgets.QLabel("Config Name : ")
        self.config_name_dropdown = QtWidgets.QComboBox()
        self.config_name_dropdown.activated.connect(self.on_select_items)
        self.populate_dropdown_config()
        self.config_name_layout.addWidget(self.config_name_label)
        self.config_name_layout.addWidget(self.config_name_dropdown)
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
        self.save_button.clicked.connect(self.on_save_configuration)
        self.bottom_buttons_layout.addWidget(self.save_button)
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setText("Export")
        self.bottom_buttons_layout.addWidget(self.export_button)
        self.load_button = QtWidgets.QPushButton()
        self.load_button.setText("Load")
        self.bottom_buttons_layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.on_load_configuration)
        #self.load_new_button = QtWidgets.QPushButton()
        #self.load_new_button.setText("Load_new")
        #self.bottom_buttons_layout.addWidget(self.load_new_button)


        self.main_layout.addLayout(self.bottom_buttons_layout)
        self.setLayout(self.main_layout)

    def set_default_values(self):
        """parse the file, foreach line, assign the value to the right parameter"""
        #get the default config file

        config_name = self.file_system.default_config_name
        index = 0
        for i in range(self.config_name_dropdown.count()):
            if(self.config_name_dropdown.itemText(i)==config_name):
                index = i
            print(self.config_name_dropdown.itemText(i) +" - "+config_name)
        self.config_name_dropdown.setCurrentIndex(index)

        #self.config_name_input.setText(config.name)
        config = self.file_system.get_config_file()
        self.update_configuration(config)

    def populate_dropdown_config(self):
        """used to populate the dropdown config name """
        print("path = "+__file__)
        files = os.listdir(self.file_system.config_folder_path)
        configs = {}
        for f in files:
            config_name = f.replace(".yml", "")
            configs[config_name] = f
        self.config_name_dropdown.addItems(configs.keys())

    def on_select_items(self,index):
        """callback for when the drop down list is changing"""
        #todo:code this part
        config_name = self.config_name_dropdown.itemText(index)
        #self.file_system.set_config(index)
        config = self.file_system.get_config(config_name)
        self.update_configuration(config)

    def update_configuration(self, config):
        self.current_config = config.name
        self.project_input.setText(config.project_directory.pattern)
        self.asset_file_name_input.setText(config.asset_file_name.pattern)
        self.asset_path_input.setText(config.asset_path.pattern)
        self.file_input.setText(config.asset_file_path.pattern)
        self.workspace_input.setText(config.workspace_path.pattern)
        self.render_input.setText(config.render_path.pattern)
        self.flip_input.setText(config.flip_path.pattern)
        self.cache_input.setText(config.caches_path.pattern)
        self.texture_input.setText(config.textures_path.pattern)

    def on_load_configuration(self):
        self.main_window.add_new_config(self.current_config)

    def on_save_configuration(self):
        text,ok = QtWidgets.QInputDialog().getText(self, "save configuration", "Config Name", QtWidgets.QLineEdit.Normal) # QFileDialog()#  QTextBrowser(minimumWidth=800,minimumHeight=800)
        print(text)
        #todo : save a config file with the good name
