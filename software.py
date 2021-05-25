import json
import os

class Software():
    """over layer to describing differnet software used with the asset"""

    @property
    def ext(self):
        return self.__ext

    @property
    def name(self):
        return self.__name

    """@property
    def engine(self):
        return self.__engine"""

    def __init__(self, name, ext):
        self.__name = name
        self.__ext = ext

    def write_JSON(self, data_type):
        pass
        # open the JSON
        # check if the data type already exist
        # if yes, load datas, add the news
        # write the datas in the JSON
        # close

    def set_json_path(self, path):
        self.__json_path = path

    def read_caches_datas(self):
        self.__json_path = self.__json_path.replace('/', r'\\')
        print("looking for file : "+str(self.__json_path))
        datas = ""
        if os.path.exists(self.__json_path):
            f = open(self.__json_path, 'r')
            json_datas = json.loads(f.read())
            if "caches" in json_datas.keys():
                datas = json_datas["caches"]
            print("datas = "+str(datas))
        return datas