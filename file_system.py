import os
import glob
import config
#config = "{assetType}/{assetName}/{workspace}/{task}/{subtask}/{versions}"
#"Buildings\Tower1\Modelisation\Modelisation\work_v003"

#"Buildings\Tower1\Modelisation\work_v003"

#asset_dir = r"C:\Users\Natspir\NatspirProd\03_WORK_PIPE\01_ASSET_3D"

class file_system_meta(type):
    '''Used to implement singleton'''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls]=instance
        return cls._instances[cls]

class file_system(metaclass=file_system_meta):
    #asset_list = []
    def __init__(self):
        self.assets = {}  # dic with {assetname, asset}
        self.__configs = {} #dic containing different pipeline configuration files (that allow to handle different projects) {configName, configClass}
        default_config_name = "default"
        self.__configs[default_config_name] = config.Config(default_config_name)
        #self.config = config.Config("default")

    def get_assets(self):
        print("get_assets = "+str(len(self.assets)))
        return self.assets

    def parse_asset_list(self, config_name = "default"):
        """todo: parse the assets folder using the config file"""
        #load the configuration file to parse the asset in the project directory
        config = self.__configs[config_name]
        config.list_templates()

        asset_dir = config.project_directory.pattern
        houdini_files = glob.glob(asset_dir+"/**/*.hipnc", recursive=True)
        houdini_assets = []
        #cleanBackuoFiles:
        for file in houdini_files:
            if "backup" not in file:
                houdini_assets.append(file)
        print("houdini_assets = "+str(houdini_assets))

        #analyze all valid paths
        for file in houdini_assets:
            file_path = file.replace(asset_dir+"\\","" )
            print("try parsing path : "+file_path)

            print(config.asset_file_path.pattern)
            datas = config.asset_file_path.parse(os.path.dirname(file_path))
            #file_datas = file_path.split("\\")
            asset_type = datas["AssetType"]
            asset_name = datas["AssetName"]
            asset_task = datas["Task"]
            print("parsing asset 'asset_name', asset_type = "+asset_type+", asset_task = "+str(asset_task))
            asset_subtask = datas["Subtask"]
            asset_work = datas["Version"]

            #looking for thumbnail :
            asset_thumbnail = ""
            picture_folder = self.get_picture_folder(file)
            if(picture_folder):
                print("######picture folder found####### : "+picture_folder)
                pics = os.listdir(picture_folder) #list all pictures
                for p in pics:
                    pic_path = picture_folder+os.sep+p
                    print("pic_path = "+pic_path+" os.path.isfile(p) = "+str(os.path.isfile(pic_path)))
                    if os.path.isfile(pic_path):
                        if ".png" in p or ".jpeg" in p: #detect if it's a valid picture
                            asset_thumbnail = pic_path
                            break


            if(asset_name not in self.assets): #if its a new asset
                print("#####new asset detected######")
                if(asset_thumbnail):
                    print("####asset_thumbnail = "+asset_thumbnail)
                new_asset = asset(asset_name,asset_type)
                new_asset.add_task(asset_task, asset_subtask, asset_work, asset_thumbnail)
                self.assets[asset_name]=new_asset
            else : #if the asset already exist
                self.assets[asset_name].add_version(asset_task, asset_subtask, asset_work, asset_thumbnail)

        for a in self.assets.keys():
             print("asset : "+a+" tasks = "+str(self.assets[a].tasks.keys()))

        print("assets = ")
        for i in self.assets.keys():
            print(i)

        #get list of all .hipnc, .blend, .ma
        #analyse their path
        #add them in the asset database

        '''config_tab = config.split("/")
        for i in range(0, len(config_tab)):
            dirs = os.listdir(asset_dir)

        print(dirs)'''

    def get_asset_type(self):
        pass

    def load_asset(self):
        pass

    def open_folder(self, asset_name, asset_type, asset_task, asset_subtask, subtask_version,config_file="default"):
        config = self.__configs[config_file]
        asset_dir = config.project_directory.pattern
        datas = {
            'AssetType' : asset_type,
            'AssetName' : asset_name,
            'Task' : asset_task,
            'Subtask' : asset_subtask,
            'Version' : subtask_version}
        print("file_path = config.asset_file_path = "+config.asset_file_path.pattern)
        file_path = config.asset_file_path.format(datas)
        folders = [asset_dir,asset_type, asset_name, asset_task, asset_subtask, subtask_version]

        path = os.path.join(*folders)
        # path = os.path.realpath(path)
        #path = path.replace("\\", "/")
        os.system(f'start {path}')

    def get_render_directory(self,datas,config_name='default'):
        config = self.__configs[config_name]
        path = config.project_directory.pattern + os.sep + config.render_path.format(datas)
        path = path.replace("\\", "/")
        return  path

    def get_flip_directory(self, datas,config_name='default'):
        config = self.__configs[config_name]
        path =config.project_directory.pattern+os.sep+ config.flip_path.format(datas)
        path = path.replace("\\","/")
        return path

    def get_picture_folder(self, file_path):
        name_filp_folder = "flip"
        name_render_folder = "render"
        picture_foler = ""
        dir_path = os.path.dirname(file_path)
        print("###look for picture at file path "+dir_path)
        list_dir = os.listdir(dir_path)
        print("###listdir = "+str(list_dir))
        for dir in list_dir :
            sub_path = dir_path+os.sep+dir
            print("os.path.isdir(dir) = "+str(os.path.isdir(sub_path)))
            if os.path.isdir(sub_path): #verify it's a directory
                dir = dir.lower() #set it to lowercase
                print("###Dir =  " + dir)
                if name_render_folder in dir:
                    picture_foler = sub_path
                    break
                elif name_filp_folder in dir :
                    picture_foler = sub_path
        return picture_foler

    def get_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                f = os.path.join(dirpath,i)
                total_size += os.path.getsize(f)
        return total_size

    def get_asset_size(self, datas, config_name = "default"):
        config = self.__configs[config_name]
        path = config.project_directory.pattern+os.sep+ config.asset_path.format(datas)
        return self.get_size(path)

class Task():
    def __init__(self, asset_name, task_name, subtask_name, version, thumbnail=""):
        self.__asset_name = asset_name
        self.__name = task_name
        subtask = Subtask(asset_name, task_name, subtask_name, version, thumbnail)
        # dictionary containing the subtask with their name : {subtask_name,subtask }
        self.subtasks = {subtask_name : subtask }
        #self.subtasks[] = subtask
        self.__current_subtask=subtask
        self.thumbnail = thumbnail

    def get_tasks(self):
        pass

    def name(self):
        return self.__name

    def add_subtask(self, subtask_name, version, thumbnail):
        """add a subtask if it doesn't already exist"""
        if(subtask_name not in self.subtasks.keys()):
            subtask = Subtask(self.__asset_name, self.__name,subtask_name, version, thumbnail)
            self.subtasks[subtask_name] = subtask

    def add_version(self, subtask_name, version, thumbnail):
        #print("tasks : add version "+subtask_name+", "+version)
        """create subtask if it doesn't exist, then add a version"""
        if(subtask_name not in self.subtasks.keys()):
            self.add_subtask(subtask_name, version, thumbnail)
        else:
            self.subtasks[subtask_name].add_version(version, thumbnail)

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
    def __init__(self, asset_name,task,subtask , name, thumbnail):
        self.__name = name
        self.__asset_name = asset_name
        self.__task = task
        self.__subtask = subtask
        self.thumbnail = thumbnail
        self.comment = ""
    def name(self):
        return self.__name

    def get_last_thumbnail(self):
        return self.thumbnail

    @property
    def datas(self):
        return {
            'AssetName' : self.__asset_name,
            'Task' : self.__task,
            'Subtask' : self.__subtask,
            'Version' : self.__name
        }

class Subtask():
    #todo : handle thumbnail for subtasks and new subtasks
    def __init__(self, asset_name, task_name, subtask_name, version, thumbnail=""):
        self.__name = subtask_name
        self.__task_name = task_name
        self.__asset_name = asset_name
        self.selected_version = Version(asset_name, task_name, subtask_name, version ,thumbnail)
        self.__versions = {}
        self.__versions[version] = self.selected_version
        self.thumbnail=self.selected_version.thumbnail

    def add_version(self, version_name, thumbnail):
        #print("add version "+version)
        if version_name not in self.__versions.keys():
            version = Version(self.__asset_name, self.__task_name, self.__name,version_name,thumbnail)
            self.__versions[version_name]=version

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
    def current_version(self):
        return self.current_task.current_subtask().selected_version

    @property
    def total_size(self):
        datas={
            "AssetName":self.name,
            "AssetType":self.type
        }
        return self.file_system.get_asset_size(datas)

    def __init__(self, name, type ):
        self.name = name
        self.type = type
        self.tasks = {} #dic of task element {task_name, Task()}
        self.current_task = None
        #self.current_version = None
        self.__thumbnails = ""
        self.file_system = file_system()

    def add_task(self, task_name, subtask_name, version, thumbnails_path):
        """Add a task if it doesn't exist. Return the new task."""
        print("####add task thumbnails_path = "+thumbnails_path)
        new_task = None
        if task_name not in self.tasks.keys(): #if it's a new task
            new_task = Task(self.name, task_name, subtask_name, version, thumbnails_path)
            self.tasks[task_name]=new_task #add the new task
            if thumbnails_path: #don't override thumbnail when its null
                print("##Add task thumbnails_path = " + thumbnails_path)
                self.__thumbnails = thumbnails_path
        return new_task

    '''def add_subtask(self, task_name, subtask_name, version, thumbnail):
        """Add a subtask if it doesn't exist."""
        if(task_name in self.tasks.keys()):#if the task already exist, juste create the task
            self.tasks[task_name].add_subtask(subtask_name, version, thumbnail)
        else: #if the task doesn't exist yet, create it and create the subtask
            self.add_task(task_name, subtask_name, version, thumbnail)'''

    def add_version(self, task_name, subtask_name, version, asset_thumbnail):
        """create the task if not exist, then add the version to the task"""
        if asset_thumbnail: #don't overide the thumbnail path if it's empty
            print("##Add version asset_thumbnail = "+asset_thumbnail)
        #print("asset : add_version "+ version)
        if(task_name not in self.tasks.keys()):
            self.add_task(task_name, subtask_name, version, asset_thumbnail)
        self.tasks[task_name].add_version(subtask_name, version, asset_thumbnail)

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
    def get_versions(self, task_name, subtask_name):
        #print("get version for task_name = "+task_name+" subtask_name = "+subtask_name)
        return self.tasks[task_name].get_current_versions()

    def get_current_versions(self):
        #print("get version for task_name = "+task_name+" subtask_name = "+subtask_name)
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
        self.file_system.open_folder(self.name, self.type, self.current_task.name(),self.current_task.current_subtask().name(), self.current_task.current_subtask().selected_version.name())

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
        print("datas = "+str(datas))
        flip_dir = self.file_system.get_flip_directory(datas)
        print("flip_dir = "+flip_dir)
        return flip_dir
        #return os.path.dirname(self.thumbnail())

    def current_render_dir(self):
        """if render directory exist return it"""
        datas = self.current_version.datas
        datas['AssetType'] = self.type
        render_dir = self.file_system.get_render_directory(datas)
        #file_system.get_render_directory(self.name, self.current_task, self.current_subtask(), self.current_version)
        return render_dir
    def get_render_folder(self):
        pass #self.asset_path+sub

    def get_last_thumbnail(self):
        thumbnail = ""
        for t in self.tasks.keys():
            temp_thumb = self.tasks[t].get_last_thumbnail()
            if temp_thumb:
                thumbnail = temp_thumb
        return thumbnail

    def thumbnail(self):
        return self.get_last_thumbnail()

if __name__ == "__main__":
    f = file_system()