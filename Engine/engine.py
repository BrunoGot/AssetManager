import json
import file_system

def get(extension):
    if "hipnc" in extension:
        from Engine import houdini_engine as he
        return he.HoudiniEngine()

class Engine():
    def __init__(self):
        fs = file_system.file_system()
        #fs.
    def write_JSON(self, data_type, datas):
        #open the JSON
        #check if the data type already exist
        #if yes, load datas, add the news
        #write the datas in the JSON
        #close
        json.loads(self.json_datas)


"""
Caches : []
Textures : []
"""