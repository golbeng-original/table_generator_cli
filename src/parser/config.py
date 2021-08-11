import os
from ruamel.yaml import YAML

class YamlObject:
    __context = None

    def __init__(self, context):
        self.__context = context

    @property
    def getcontext(self):
        return self.__context

    def get_value(self, path:str):
        object = self.get_object(path)
        if not object:
            return None

        return object.getcontext

    def get_object(self, path:str):
        elements = path.split('.')
        
        current_context = self.__context
        for element in elements:

            if not isinstance(current_context, dict):
                return None

            if element not in current_context:
                return None

            current_context = current_context[element]

        return YamlObject(current_context)


class YamlConfig:

    __root_object:YamlObject = None

    def __init__(self, config_path:str):
        _, ext = os.path.splitext(config_path)
        if ext.lower() != '.yaml':
            raise Exception('{0} file is not yaml file'.format(config_path))

        with open(config_path, 'r') as f:
            yaml = YAML()
            yaml_context = yaml.load(f)

            self.__root_object = YamlObject(yaml_context)
        
    def get_object(self, path:str):
        return self.__root_object.get_object(path)

    def get_value(self, path:str):
        object = self.get_object(path)
        if not object:
            return None

        return object.getcontext


