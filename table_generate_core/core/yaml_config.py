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

class GenerateYamlObject(YamlObject):

    def __init__(self, context):
        super().__init__(context)

    @property
    def db_extension(self):
        return self.get_value('db_extension')

    @property
    def namespace(self):
        return self.get_value('namespace')

    @property
    def class_generate_path(self):
        return self.get_value('generate_path.path')

    @property
    def class_generate_usings(self):
        usings = self.get_value('generate_path.usings')
        if not isinstance(usings, list):
            return []

        return usings

    @property
    def class_generate_imports(self):
        imports = self.get_value('generate_path.imports')
        if not isinstance(imports, list):
            return []

        return imports

    @property
    def meta_generate_path(self):
        return self.get_value('meta_generate_path.path')

    @property
    def meta_entry_info(self):
        entry_class = self.get_value('meta_generate_path.entry_class')
        entry_name = self.get_value('meta_generate_path.entry_name')

        return (entry_class, entry_name)

    @property
    def meta_generate_usings(self):
        usings = self.get_value('meta_generate_path.usings')
        if not isinstance(usings, list):
            return []

        return usings

    @property
    def meta_generate_imports(self):
        imports = self.get_value('meta_generate_path.imports')
        if not isinstance(imports, list):
            return []

        return imports

    @property
    def meta_collection(self):
        return self.get_value('meta_generate_path.meta_collection')

class EnumYamlObject(YamlObject):

    @property
    def language(self):
        return self.get_value('language')

    @property
    def generate_path(self):
        return self.get_value('path')

    @property
    def namespace(self):
        return self.get_value('namespace')

class DataYamlObject(YamlObject):
    
    @property
    def language(self):
        return self.get_value('language')

    @property
    def generate_path(self):
        return self.get_value('path')

    @property
    def db_extension(self):
        return self.get_value('db_extension')

class CollectionYamlObject(YamlObject):

    @property
    def schema_file_glob(self):
        return self.get_value('schema_file_glob')

    @property
    def data_file_glob(self):
        return self.get_value('data_file_glob')

    @property
    def enum_define_file_glob(self):
        return self.get_value('enum_define_file_glob')

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

    def get_class_generate_config(self, language:str, path:str = 'class_generate_config'):
        class_genreate_config = self.get_value(path)
        
        if not class_genreate_config:
            return None

        if not  isinstance(class_genreate_config, list):
            return None

        for generate_element in class_genreate_config:
            yaml_object = GenerateYamlObject(generate_element)

            lang = yaml_object.get_value('language')
            if lang == language:
                return yaml_object

        return None

    def get_collection_config(self, path:str = 'collection_config'):
        collectio_config_object = CollectionYamlObject(self.get_value(path))
        return collectio_config_object

    def get_enum_generate_config(self, language:str, path:str = 'enum_generate_config'):
        enum_genreate_configs = self.get_value(path + '.generate')
        
        if not isinstance(enum_genreate_configs, list):
            return None

        for enum_generate_config in enum_genreate_configs:
            enum_yaml_object = EnumYamlObject(enum_generate_config)
            if enum_yaml_object.language == language:
                return enum_yaml_object

        return None

    def get_data_generate_config(self, language:str, path:str = 'data_generate_config'):
        raw_db_configs = self.get_value(path)

        if not isinstance(raw_db_configs, list):
            return None

        for raw_db_config in raw_db_configs:
            db_config = DataYamlObject(raw_db_config)
            if db_config.language == language:
                return db_config

        return None

