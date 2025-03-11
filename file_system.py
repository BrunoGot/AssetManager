import glob
import os

import config
from software import Software


class file_system_meta(type):
    '''Used to implement singleton'''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class file_system(metaclass=file_system_meta):
    """
    This class is supposed to do the link between the file system of the current operating system
    and the file system defined by the pipeline configuration files.
    It have been set as a singleton class that contain different configutaion type. This allow th user to switch
    from a project to another with different configuration for each project.
    This class is supposed to be used as a singleton tho, as it the same object that is used to load
    and interact ith the different project.
    """

    @property
    def config_folder_path(self):
        return self.__config_folder_path

    def __init__(self):
        # folder containing the configuration files
        self.__config_folder_path = os.path.dirname(__file__) + r"/Configurations"

        self.init_configs()

        self.assets_configs = {
            self.__current_config_name: {}}  # dic wit {config_name, self.assets} #link the list of asset associated to the
        self.assets = self.assets_configs  # dic with {assetname, asset} todo: will be renamed as current_assets
        # self.config = config.Config("default")

    def init_configs(self):
        self.__configs = {}  # dic containing different pipeline configuration files (that allow to handle different projects) {configName, configClass}
        configs = self.__get_config_list()
        for name, path in configs.items():
            print("path = " + path)
            self.__configs[name] = config.Config(name, path)
        self.default_config_name = "My_Projects"
        self.__current_config_name = self.default_config_name
        self.__configs[self.__current_config_name] = config.Config(self.__current_config_name)

    def __get_config_list(self):
        """
        list the yml file in the config folder and return a dictionary {config_name, config_path}
        """

        files = os.listdir(self.__config_folder_path)
        configs = {}
        for f in files:
            config_name = f.replace(".yml", "")
            configs[config_name] = self.__config_folder_path + os.sep + f
        return configs

    def get_configs(self):
        return self.__configs

    def get_assets(self):
        print("get_assets = " + str(len(self.assets)))
        return self.assets

    def parse_asset_list(self):
        """todo: parse the assets folder using the config file"""
        # load the configuration file to parse the asset in the project directory
        config = self.__configs[self.__current_config_name]
        config.list_templates()

        asset_dir = config.project_directory.pattern
        houdini_files = glob.glob(asset_dir + "/**/*.hipnc", recursive=True)
        blender_files = glob.glob(asset_dir + "/**/*.blend", recursive=True)
        asset_files = blender_files + houdini_files
        assets = []
        # cleanBackuoFiles:
        for file in asset_files:
            if "backup" not in file:
                assets.append(file)
        print("houdini_assets = " + str(assets))

        # analyze all valid paths
        for file in assets:
            file_path = file.replace(asset_dir + "\\", "")
            print("try parsing path : " + file_path)
            print(config.asset_file_path.pattern)
            try:
                asset_dir_datas = config.asset_file_path.parse(file_path)
                asset_file_name_data = config.asset_file_name.parse(os.path.basename(file_path))
                # file_datas = file_path.split("\\")
                asset_type = asset_dir_datas.get("AssetType")
                if not asset_type:
                    asset_type = ""
                asset_name = asset_dir_datas["AssetName"]
                asset_task = asset_dir_datas["Task"]
                print("parsing asset 'asset_name', asset_type = " + asset_type + ", asset_task = " + str(asset_task))
                asset_subtask = asset_dir_datas.get("Subtask")
                if not asset_subtask:
                    asset_subtask = ""
                asset_work = asset_dir_datas["Version"]
                asset_file_name = asset_file_name_data["AssetFileName"]
                asset_ext = asset_file_name_data["Ext"]
                print(asset_file_name + asset_ext)

                # looking for thumbnail :
                asset_thumbnail = ""
                picture_folder = self.get_picture_folder(file)
                if (picture_folder):
                    # print("######picture folder found####### : "+picture_folder)
                    pics = os.listdir(picture_folder)  # list all pictures
                    for p in pics:
                        pic_path = picture_folder + os.sep + p
                        # print("pic_path = "+pic_path+" os.path.isfile(p) = "+str(os.path.isfile(pic_path)))
                        if os.path.isfile(pic_path):
                            if ".png" in p or ".jpeg" in p or "jpg" in p:  # detect if it's a valid picture
                                asset_thumbnail = pic_path
                                break

                if (asset_name not in self.assets):  # if its a new asset
                    print("#####new asset detected######")
                    if (asset_thumbnail):
                        print("####asset_thumbnail = " + asset_thumbnail)
                    new_asset = asset(asset_name, asset_type)
                    new_asset.add_task(asset_task, asset_subtask, asset_work, asset_file_name, asset_ext,
                                       asset_thumbnail)
                    self.assets[asset_name] = new_asset
                else:  # if the asset already exist
                    self.assets[asset_name].add_version(asset_task, asset_subtask, asset_work, asset_file_name,
                                                        asset_ext, asset_thumbnail)
            except Exception as e:
                print(f"#####ERROR : asset not parsed correctly : {file_path} | err = {e.args}")

        for a in sorted(self.assets):
            print("asset : " + a + " tasks = " + str(self.assets[a].tasks.keys()))

        print("assets = ")
        for i in self.assets.keys():
            print(i)

        # get list of all .hipnc, .blend, .ma
        # analyse their path
        # add them in the asset database

        '''config_tab = config.split("/")
        for i in range(0, len(config_tab)):
            dirs = os.listdir(asset_dir)

        print(dirs)'''

    def get_asset_type(self):
        pass

    def load_asset(self):
        pass

    def get_filtered_files(self, dir_path, extensions):
        """
        return a list of file containing in the directory path end ing with the extension in the list
        :param str dir_path: path to the directory to look into
        :param [str] extensions: list of extensions we want to get
        :return [str] filtered_files: list of filename corresponding to the filter in this folder
        """
        filtered_files = []
        if os.path.exists(dir_path):
            filtered_files = [f for f in os.listdir(dir_path) if any(f.endswith(ext) for ext in extensions)]
        return filtered_files

    def open_folder(self, datas, ):
        config = self.__configs[self.__current_config_name]
        asset_dir = config.project_directory.pattern

        print("file_path = config.asset_file_path = " + config.asset_file_path.pattern)
        file_path = config.asset_file_path.format(datas)
        folders = [asset_dir, file_path]

        path = os.path.join(*folders)
        os.system(f'start {path}')

    def get_version_file_path(self, version_datas):
        """
        open the file corresponding to the given datas
        :param dic{} version_datas: dictionary like 'AssetType' : self.__asset_type see Version.datas
        """

        config = self.__configs[self.__current_config_name]
        print("datas = " + str(version_datas))
        path = os.path.join(config.project_directory.pattern, config.asset_file_path.format(
            version_datas), config.asset_file_name.format(version_datas))
        return path

    def open_file(self, datas):
        """
        open the file corresponding to the given datas
        :param dic{} datas: dictionary from Version.datas
        """

        path = self.get_path_file(datas)
        os.system(f'start {path}')

    def get_render_directory(self, datas):
        config = self.__configs[self.__current_config_name]
        path = config.project_directory.pattern + os.sep + config.render_path.format(datas)
        path = path.replace("\\", "/")
        return path

    def get_cache_directory(self, datas):
        config = self.__configs[self.__current_config_name]
        return self.get_directory_path(config, datas, config.caches_path)

    def get_directory_path(self, config, datas, config_template_type):
        """
        todo: the deal with this functin is to avoid redondance in between get_cache_dir, get_render_dir etc.
        return the formatted path according to the type of path contained by config_path_type
        :param Config config: the configuration to use the template from.
        :param datas: dic of element to fill the template with
        :param config_template_type: template path from config.py config.caches_path or config.render_path
        :return str: path to teh desired folder (cache, render, flip)
        """

        path = os.path.join(config.project_directory.pattern, config_template_type.format(datas))
        path = path.replace("\\", "/")
        return path

    def get_flip_directory(self, datas):
        config = self.__configs[self.__current_config_name]
        path = config.project_directory.pattern + os.sep + config.flip_path.format(datas)
        path = path.replace("\\", "/")
        return path

    def get_picture_folder(self, file_path):
        name_filp_folder = "flip"
        name_render_folder = "render"
        picture_foler = ""
        dir_path = os.path.dirname(file_path)
        # print("###look for picture at file path "+dir_path)
        list_dir = os.listdir(dir_path)
        # print("###listdir = "+str(list_dir))
        for dir in list_dir:
            sub_path = dir_path + os.sep + dir
            # print("os.path.isdir(dir) = "+str(os.path.isdir(sub_path)))
            if os.path.isdir(sub_path):  # verify it's a directory
                dir = dir.lower()  # set it to lowercase
                # print("###Dir =  " + dir)
                if name_render_folder in dir:
                    picture_foler = sub_path
                    break
                elif name_filp_folder in dir:
                    picture_foler = sub_path
        return picture_foler

    def get_size(self, path):
        total_size = 0
        # path=path.replace("\\", "/")
        print("get_size path = " + path)
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                f = os.path.join(dirpath, i)
                # print("f = "+f)
                total_size += os.path.getsize(f)
        total_size = total_size / (1024 * 1024)
        total_size = round(total_size, 2)
        return total_size

    def get_file_size(self, file_path):
        size = os.path.getsize(file_path)
        size = size / (1024 * 1024)
        return round(size, 2)

    def get_version_size(self, datas):
        config = self.__configs[self.__current_config_name]
        path = config.project_directory.pattern + os.sep + config.asset_file_path.format(datas)
        return self.get_size(path)

    def get_asset_size(self, datas):
        config = self.__configs[self.__current_config_name]
        path = config.project_directory.pattern + os.sep + config.asset_path.format(datas)
        return self.get_size(path)

    def detect_software(self, ext):
        """return the software associated to the selected verion in datas"""
        software = None
        print("ext = " + ext)
        software = self.get_software(ext)
        return software

    def get_software(self, ext):
        """return the software name according to its extenxion"""
        soft_name = ""
        soft = None
        print("ext = " + ext)
        if (ext == "hipnc"):
            soft_name = "Houdini"
        elif (ext == "blend"):
            soft_name = "Blender"
        if (soft_name != ""):
            soft = Software(soft_name, ext)
        return soft

    def get_config_file(self):
        """return the current config"""
        return self.__configs[self.default_config_name]

    def get_config(self, config_name):
        """return the config at the given name"""
        config = self.__configs[self.default_config_name]
        if config_name in self.__configs.keys():  # check if the config exist in the dic
            config = self.__configs[config_name]
        return config

    def save_comment(self, datas, text):
        """write the text in a text file"""
        config = self.__configs[self.__current_config_name]
        file_name = "comment.txt"  # todo:move it in the config section
        path = config.project_directory.pattern + os.sep + config.asset_file_path.format(datas) + os.sep + file_name
        f = open(path, "w")
        f.write(text)
        f.close()

    def load_comment(self, datas):
        config = self.__configs[self.__current_config_name]
        file_name = "comment.txt"  # todo:move it in the config section
        path = config.project_directory.pattern + os.sep + config.asset_file_path.format(datas) + os.sep + file_name
        text = ""
        if os.path.exists(path):
            f = open(path, "r")
            text = f.read()
            f.close()
        return text

    def get_engine_json(self, datas):
        config = self.__configs[self.__current_config_name]
        path = config.project_directory.pattern + os.sep + config.json_engine.format(datas)
        print("json path = " + path)
        return path

    def set_current_config(self, config_name):
        if config_name not in self.assets_configs:
            self.assets_configs[config_name] = {}
        self.assets = self.assets_configs[config_name]
        self.__current_config_name = config_name

    def set_current_config_index(self, config_index):
        keys = list(self.assets_configs.keys())
        print("keys = {}".format(keys))
        config_name = keys[config_index]
        self.set_current_config(config_name)
        print("switch to config_name : " + config_name)


######################"

class Task():
    def __init__(self, asset_type, asset_name, task_name, subtask_name, version, file_name, ext, thumbnail=""):
        self.__asset_name = asset_name
        self.__name = task_name
        self.__asset_type = asset_type
        subtask = Subtask(asset_type, asset_name, task_name, subtask_name, version, file_name, ext, thumbnail)
        # dictionary containing the subtask with their name : {subtask_name,subtask }
        self.subtasks = {subtask_name: subtask}
        # self.subtasks[] = subtask
        self.__current_subtask = subtask
        self.thumbnail = thumbnail

    def get_tasks(self):
        pass

    def name(self):
        return self.__name

    def add_subtask(self, subtask_name, version, file_name, ext, thumbnail):
        """add a subtask if it doesn't already exist"""
        if (subtask_name not in self.subtasks.keys()):
            subtask = Subtask(self.__asset_type, self.__asset_name, self.__name, subtask_name, version, file_name, ext,
                              thumbnail)
            self.subtasks[subtask_name] = subtask

    def add_version(self, subtask_name, version, file_name, ext, thumbnail):
        # print("tasks : add version "+subtask_name+", "+version)
        """create subtask if it doesn't exist, then add a version"""
        if (subtask_name not in self.subtasks.keys()):
            self.add_subtask(subtask_name, version, file_name, ext, thumbnail)
        else:
            self.subtasks[subtask_name].add_version(version, file_name, ext, thumbnail)

    def get_subtasks(self):
        return self.subtasks

    def get_current_versions(self):
        return self.subtasks[self.__current_subtask.name()].get_versions()

    def set_current_subtask(self, subtask_name):
        self.__current_subtask = self.subtasks[subtask_name]

    def current_subtask(self):
        return self.__current_subtask

    def get_last_thumbnail(self):
        thumbnail = ""
        for s in self.subtasks.keys():
            temp_thumb = self.subtasks[s].get_last_thumbnail()
            if temp_thumb:
                thumbnail = temp_thumb
        return thumbnail


class Version():
    def __init__(self, asset_type, asset_name, task, subtask, name, file_name, ext, thumbnail):
        self.__name = name
        self.__asset_type = asset_type
        self.__asset_name = asset_name
        self.__task = task
        self.__subtask = subtask
        self.thumbnail = thumbnail
        self.comment = ""
        self.__file_name = file_name  # the name of the asset file
        self.__ext = ext  # the name of the extension
        self.file_system = file_system()
        self.__software = self.file_system.detect_software(ext)

        # set the path to get the json software data
        path = self.file_system.get_engine_json(self.datas)
        print("JSON PATH = " + path)
        self.__software.set_json_path(path)
        # datas = self.datas

    def name(self):
        return self.__name

    def get_last_thumbnail(self):
        return self.thumbnail

    def set_comment(self, text):
        self.__name = text

    @property
    def software(self):
        return self.__software

    @property
    def datas(self):
        return {
            'AssetType': self.__asset_type,
            'AssetName': self.__asset_name,
            'Task': self.__task,
            'Subtask': self.__subtask,
            'Version': self.__name,
            'AssetFileName': self.__file_name,
            'Ext': self.__ext,
            'Engine_name': self.__software.name
        }

    def get_caches_datas(self):
        caches = self.software.read_caches_datas()
        return caches

    def update_datas(self):
        pass
        # update the json_engine with the last datas in the software (caches, textures)
        # self.engine.update_datas
        # self.enfine.get_datas


class Subtask():
    # todo : handle thumbnail for subtasks and new subtasks
    def __init__(self, asset_type, asset_name, task_name, subtask_name, version, file_name, ext, thumbnail=""):
        self.__asset_type = asset_type
        self.__name = subtask_name
        self.__task_name = task_name
        self.__asset_name = asset_name
        self.selected_version = Version(asset_type, asset_name, task_name, subtask_name, version, file_name, ext,
                                        thumbnail)
        self.__versions = {}
        self.__versions[version] = self.selected_version
        self.set_current_version(version)
        self.thumbnail = self.selected_version.thumbnail

    def add_version(self, version_name, file_name, ext, thumbnail):
        """
        :param version_name:
        :param file_name:
        :param ext:
        :param thumbnail:
        """

        if version_name not in self.__versions.keys():
            version = Version(self.__asset_type, self.__asset_name, self.__task_name, self.__name, version_name,
                              file_name, ext, thumbnail)
            self.__versions[version_name] = version
        print("ADDVERSION")
        self.set_current_version(version_name)

    def get_versions(self):
        return self.__versions

    def set_current_version(self, version_name):
        self.selected_version = self.__versions[version_name]

    def name(self):
        return self.__name

    def get_last_thumbnail(self):
        thumbnail = ""
        for v in self.__versions.keys():
            temp_thumb = self.__versions[v].get_last_thumbnail()
            if temp_thumb:
                thumbnail = temp_thumb
        return thumbnail


class asset():

    @property
    def last_modification(self):
        return self._last_modification

    @property
    def current_version(self):
        # print("try something")
        # print(f"self.current_task = {self.current_task}")
        return self.current_task.current_subtask().selected_version

    @property
    def total_size(self):
        datas = {
            "AssetName": self.name,
            "AssetType": self.type
        }
        return self.file_system.get_asset_size(datas)

    def __init__(self, name, type=""):
        self.name = name
        self.type = type
        self.tasks = {}  # dic of task element {task_name, Task()}
        self.current_task = None
        self.__thumbnails = ""
        self.file_system = file_system()
        self._last_modification = None

    def add_task(self, task_name, subtask_name, version, file_name, ext, thumbnails_path):
        """Add a task if it doesn't exist. Return the new task."""
        print("####add task thumbnails_path = " + thumbnails_path)
        new_task = None
        if task_name not in self.tasks.keys():  # if it's a new task
            new_task = Task(self.type, self.name, task_name, subtask_name, version, file_name, ext, thumbnails_path)
            self.tasks[task_name] = new_task  # add the new task
            self.set_current_task(task_name)
            print(f"assetNamee = {self.name}")
            print(f"updatess {self.current_version}")
            self.update_last_modified_file(self.current_version.datas)
            if thumbnails_path:  # don't override thumbnail when its null
                print("##Add task thumbnails_path = " + thumbnails_path)
                self.__thumbnails = thumbnails_path
        return new_task

    '''def add_subtask(self, task_name, subtask_name, version, thumbnail):
        """Add a subtask if it doesn't exist."""
        if(task_name in self.tasks.keys()):#if the task already exist, juste create the task
            self.tasks[task_name].add_subtask(subtask_name, version, thumbnail)
        else: #if the task doesn't exist yet, create it and create the subtask
            self.add_task(task_name, subtask_name, version, thumbnail)'''

    def add_version(self, task_name, subtask_name, version, file_name, ext, asset_thumbnail):
        """
        create the task if not exist, then add the version to the task
        :param str file_name: name of the file without any path
        """
        if asset_thumbnail:  # don't overide the thumbnail path if it's empty
            print("##Add version asset_thumbnail = " + asset_thumbnail)
        # print("asset : add_version "+ version)
        if (task_name not in self.tasks.keys()):
            self.add_task(task_name, subtask_name, version, file_name, ext, asset_thumbnail)
        self.tasks[task_name].add_version(subtask_name, version, file_name, ext, asset_thumbnail)
        # checking for the last modification file path
        print("UPDATEMODIFIEDPATH")
        self.update_last_modified_file(self.current_version.datas)
        """#self.task. (task)
        if(task in self.tasks): #if the task already exist, add the subtask
            if(subtask in self.tasks[task]):
                self.versions[subtask].append(version) #we add a new version to the subtask
            else:
                self.tasks[task].append(subtask)
                self.versions[subtask] = [version]
        else: #else add the task and the subtask
            self.tasks[task] = [subtask]
            self.versions[subtask] = [version]
        """

    def update_last_modified_file(self, version_datas):
        """
        :param Version.datas version_datas:
        :return:
        """
        print(f"file_pathh = {version_datas}")
        file_path = self.file_system.get_version_file_path(version_datas)
        last_modified_path = os.path.getmtime(file_path)
        if not self._last_modification:
            self._last_modification = last_modified_path

    def get_versions(self, task_name, subtask_name):
        # print("get version for task_name = "+task_name+" subtask_name = "+subtask_name)
        return self.tasks[task_name].get_current_versions()

    def get_current_versions(self):
        # print("get version for task_name = "+task_name+" subtask_name = "+subtask_name)
        return self.current_task.get_current_versions()

    def get_subtasks(self, task_name):
        return self.tasks[task_name].get_subtasks()

    def set_current_task(self, task_name):
        self.current_task = self.tasks[task_name]

    def current_subtask(self):
        return self.current_task.current_subtask()

    def set_current_subtask(self, subtask_name):
        self.current_task.set_current_subtask(subtask_name)

    def set_current_version(self, version_name):
        self.current_task.current_subtask().set_current_version(version_name)

    def open_folder(self):
        self.file_system.open_folder(self.current_version.datas)

    def open_file(self):
        datas = self.current_version.datas
        datas['AssetType'] = self.type
        print("software = " + self.current_version.software.ext)
        self.file_system.open_file(datas)

    def CurrentFlipDir(self):
        """return the flip/render folder path of the current task/subtask/work
        check if the render folder contains an image sequence, else looking for playblast. If no playblast, just return the last render frame
        begin implementation
        thumbnail = self.thumbnail()
        flip_dir = self.get_render_folder()
        #check number of file
        if(os.path.exists(flip_dir) == False or os.listdir(flip_dir)<=1):
            flip_dir = self.get_flip_folder()
            if( not os.path.exists(flip_dir)):
                flip_dir = os.path.dirname(self.thumbnail())
        """
        datas = self.current_version.datas
        datas['AssetType'] = self.type
        print("datas = " + str(datas))
        flip_dir = self.file_system.get_flip_directory(datas)
        print("flip_dir = " + flip_dir)
        return flip_dir
        # return os.path.dirname(self.thumbnail())

    def get_current_version_dir(self):
        version_dir = os.path.dirname(self.file_system.get_version_file_path(self.datas_info))
        return version_dir

    def current_render_dir(self):
        """if render directory exist return it"""
        datas = self.current_version.datas
        datas['AssetType'] = self.type
        render_dir = self.file_system.get_render_directory(datas)
        # file_system.get_render_directory(self.name, self.current_task, self.current_subtask(), self.current_version)
        return render_dir

    def get_current_caches_dir(self):
        """
        return the cache folder path of the current version of the asset
        """
        cache_dir = self.file_system.get_cache_directory(self.datas_info)
        return cache_dir

    @property
    def datas_info(self):
        """return the data dic for this Asset"""
        datas = self.current_version.datas
        datas['AssetType'] = self.type
        return datas

    def get_render_folder(self):
        pass  # self.asset_path+sub

    def get_last_thumbnail(self):
        thumbnail = ""
        for t in self.tasks.keys():
            temp_thumb = self.tasks[t].get_last_thumbnail()
            if temp_thumb:
                thumbnail = temp_thumb
        return thumbnail

    def thumbnail(self):
        return self.get_last_thumbnail()

    def save_comment(self, text):
        datas = self.current_version.datas
        self.file_system.save_comment(datas, text)

    def get_comment(self):
        datas = self.current_version.datas
        return self.file_system.load_comment(datas)

    """def get_caches(self):
        return the list of caches of the current asset file
    """

    def get_caches_datas(self):
        cache_dir_path = self.get_current_caches_dir()
        print(f"update caches datas {cache_dir_path}")
        if not os.path.exists(cache_dir_path):
            list_info_caches = ["No Caches have been saved"]
        else:
            caches = os.listdir(cache_dir_path)
            list_info_caches = []
            # set info for each cache line
            for cache in caches:
                cache_path = os.path.join(cache_dir_path, cache)
                size = self.file_system.get_file_size(cache_path)
                list_info_caches.append(f"{cache} - {size:,}")
            # this is for caches metadatas stored in a json file : caches = self.current_version.get_caches_datas()
        return list_info_caches


if __name__ == "__main__":
    f = file_system()
