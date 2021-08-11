import os
from parser.enum_define_parser import EnumMetaData

class EnumGenerator:
    enum_meta_data:EnumMetaData = None

    def __init__(self, enum_meta_data:EnumMetaData):
        self.enum_meta_data = enum_meta_data

    def generate(self, target_path:str):
        pass

class CSharpEnumGenerator(EnumGenerator):
    '''
    C#용 Enum 생성
    '''

    __namespace:str = ''

    def __init__(self, enum_meta_data:EnumMetaData, namespace:str = ''):
        super().__init__(enum_meta_data)
        self.__namespace = namespace

    def __is_exist_namespace(self):
        return True if self.__namespace else False
    
    def generate(self, target_path:str):
        try:
            
            if target_path.endswith('.cs') == False:
                raise Exception('target_path is not cs file')

            absolute_target_path = os.path.abspath(target_path)
            dirs = os.path.dirname(absolute_target_path)
            os.makedirs(dirs, exist_ok=True)

            enum_content = ''
            if self.__is_exist_namespace():
                enum_content = 'namespace {0}\n'.format(self.__namespace)
                enum_content += '{\n'

            for enum_meta_info in self.enum_meta_data.enum_meta_infos:
                enum_unit:str = enum_meta_info.to_csharp()

                if self.__is_exist_namespace():
                    new_enum_unit = ''
                    for unit in enum_unit.splitlines(keepends=True):
                        new_enum_unit += '\t' + unit

                    enum_unit = new_enum_unit

                enum_content += enum_unit

            if self.__is_exist_namespace():
                enum_content += '}\n'

            with open(absolute_target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

class DartEnumGenerator(EnumGenerator):
    '''
    Dart용 Enum 생성
    '''

    def __init__(self, enum_meta_data:EnumMetaData):
        super().__init__(enum_meta_data)

    def generate(self, target_path: str):
        try:
            if target_path.endswith('.dart') == False:
                raise Exception('target_path is not dart file')

            absolute_target_path = os.path.abspath(target_path)
            dirs = os.path.dirname(absolute_target_path)
            os.makedirs(dirs, exist_ok=True)

            enum_content = ''
            for enum_meta_info in self.enum_meta_data.enum_meta_infos:
                enum_unit = enum_meta_info.to_dart()
                enum_content += enum_unit

            enum_content += '\n'
            enum_content += self.__generate_enum_get_index_func()

            with open(absolute_target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

    def __generate_enum_get_index_func(self):
        builder = ''
        builder += 'int getGenerateEnumIndex(dynamic value) {\n'

        for enum_meta_info in self.enum_meta_data.enum_meta_infos:
            builder += '\tif (value is {0}) {{\n'.format(enum_meta_info.enum_name)
            builder += '\t\treturn value.index;\n'
            builder += '\t}\n'

        builder += '\treturn 0;\n'
        builder += '}\n'

        return builder