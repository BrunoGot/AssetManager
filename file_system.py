import os
import glob
import config
config = "{assetType}/{assetName}/{workspace}/{task}/{subtask}/{versions}"
#"Buildings\Tower1\Modelisation\Modelisation\work_v003"

#"Buildings\Tower1\Modelisation\work_v003"

asset_dir = r"C:\Users\Natspir\NatspirProd\03_WORK_PIPE\01_ASSET_3D"

class file_system():
    #asset_list = []
    assets = {}  # dic with {assetname, asset}
    def __init__(self):
        self.parse_asset_list()
        #self.config = config.Config("default")

    def get_assets(self):
        print("get_assets = "+str(len(self.assets)))
        return self.assets

    def parse_asset_list(self):

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
            file_datas = file_path.split("\\")
            asset_type = file_datas[0]
            asset_name = file_datas[1]
            asset_task = file_datas[2]
            print("parsing asset 'asset_name', asset_type = "+asset_type+", asset_task = "+str(asset_task))
            asset_subtask = file_datas[3]
            asset_work = file_datas[4]
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



        config_tab = config.split("/")
        for i in range(0, len(config_tab)):
            dirs = os.listdir(asset_dir)

        print(dirs)
        pass

    def get_asset_type(self):
        pass

    def load_asset(self):
        pass

    def open_folder(asset_name, asset_type, asset_task, asset_subtask, subtask_version):
        folders = [asset_dir,asset_type, asset_name, asset_task, asset_subtask, subtask_version]
        path = os.path.join(*folders)
        # path = os.path.realpath(path)
        #path = path.replace("\\", "/")
        os.system(f'start {path}')

    def get_render_directory(self):
        #return render_path
        pass

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

class Task():
    def __init__(self, name, subtask_name, version, thumbnail=""):
        self.__name = name
        subtask = Subtask(subtask_name, version, thumbnail)
        self.subtasks = {}
        self.subtasks[subtask_name] = subtask #dictionary containing the subtask with their name : {subtask_name,subtask }
        self.__current_subtask=subtask
        self.thumbnail = thumbnail

    def get_tasks(self):
        pass

    def name(self):
        return self.__name

    def add_subtask(self, subtask_name, version, thumbnail):
        """add a subtask if it doesn't already exist"""
        if(subtask_name not in self.subtasks.keys()):
            subtask = Subtask(subtask_name, version, thumbnail)
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
    def __init__(self, name, thumbnail):
        self.__name = name
        self.thumbnail = thumbnail
        self.comment = ""
    def name(self):
        return self.__name

    def get_last_thumbnail(self):
        return self.thumbnail

class Subtask():
    #todo : handle thumbnail for subtasks and new subtasks
    def __init__(self, name, version, thumbnail=""):
        self.__name = name
        self.selected_version = Version(version, thumbnail)
        self.__versions = {}
        self.__versions[version] = self.selected_version
        self.thumbnail=self.selected_version.thumbnail

    def add_version(self, version_name, thumbnail):
        #print("add version "+version)
        if version_name not in self.__versions.keys():
            version = Version(version_name,thumbnail)
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
    def __init__(self, name, type ):
        self.name = name
        self.type = type
        self.tasks = {} #dic of task element {task_name, Task()}
        self.current_task = None
        #self.current_version = None
        self.__thumbnails = ""

    def add_task(self, task_name, subtask_name, version, thumbnails_path):
        """Add a task if it doesn't exist. Return the new task."""
        print("####add task thumbnails_path = "+thumbnails_path)
        new_task = None
        if task_name not in self.tasks.keys(): #if it's a new task
            new_task = Task(task_name, subtask_name, version, thumbnails_path)
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
        file_system.open_folder(self.name, self.type, self.current_task.name(),self.current_task.current_subtask().name(), self.current_task.current_subtask().selected_version.name())

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
        return os.path.dirname(self.thumbnail())

    def current_render_dir(self):
        """if render directory exist return it"""
        #file_system.get_render_directory(self.name, self.current_task, self.current_subtask(), self.current_version)
        return ""
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