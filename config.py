"""This script load config file and parse it to return location of the different folder of the VFX pipeline => Config.render_path"""

#todo : test with severals variables in the same configuration path
#process parsing yaml variables : regex replace/regex.sub
"""idea : 
    - export file configuration from pipeline side (the part taht is saving the asset)
    - configuration file preset, import/export
"""

import yaml
import lucidity

class Config():

    @property
    def json_engine(self):
        return self.__templates["JSONEngine"]

    @property
    def asset_path(self):
        return self.__templates["AssetPath"]

    @property
    def project_directory(self):
        return self.__templates["Project"]

    @property
    def asset_file_path(self):
        return self.__templates["File"]

    @property
    def asset_file_name(self):
        return self.__templates["AssetFileName"]

    @property
    def workspace_path(self):
        return self.__templates["Workspace"]

    @property
    def caches_path(self):
        return self.__templates["Caches"]

    @property
    def render_path(self):
        return self.__templates["Render"]

    @property
    def flip_path(self):
        return self.__templates["Flip"]

    @property
    def textures_path(self):
        return self.__templates["Textures"]

    @property
    def name(self):
        return self.__name

    def __init__(self, name, config_path = "../Configurations/My_Projects.yml"):
        self.key_value = ["$Project", "$AssetPath", "$File", "$Workspace", "$Caches", "$Render", "$Flip", "$Textures", "$AssetFileName"] #
        #dictionary of lucidity template
        self.__name = name
        self.__templates = self.parsing_config_file(config_path)

    def parsing_config_file(self, config_file):
        """parse the yaml file and return some lucidity patterns """
        templates = {}
        #parsing the config yml file
        yaml_file = open(config_file, 'r')
        yaml_content = yaml.safe_load(yaml_file)

        print("key : value")
        for key, value in yaml_content.items():
            print(f"{key}: {value}")
            if("$" in value): #detect a keyvalue in the string
                for i in self.key_value: #determine wich key is it
                    if i in value: #if the detected key has been found
                        detected_key = i.replace("$", '') #delete the "$" symbol
                        value = value.replace(i,yaml_content[detected_key] ) #assign the new value
                        yaml_content[key] = value
                        #print("new value = "+yaml_content[key])
            templates[key] = lucidity.Template(key, yaml_content[key])
        return templates

    def list_templates(self):
        print("##list templates : ")
        for key, value in self.__templates.items():
            print(f"{key}: {value.pattern}")
    #test lucidity
    """template_file = lucidity.Template('file', yaml_content["File"])
    template_workspace = lucidity.Template('workspace', yaml_content["Workspace"])
    template_render = lucidity.Template('render', yaml_content["Render"])
    print(template_file.pattern)
    print(template_workspace.pattern)
    print(template_render.pattern)"""