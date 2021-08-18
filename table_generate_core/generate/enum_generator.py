import os
from parser.enum_define_parser import EnumMetaData
from core.path_util import convert_path, mkdir_path
from core.yaml_config import YamlConfig, EnumYamlObject
from generate.generate_struct import ConvertTargetType

class EnumGenerator:
    _enum_config:EnumYamlObject = None

    def __init__(self, yaml_config:YamlConfig, convert_type:ConvertTargetType):
        self._enum_config = yaml_config.get_enum_generate_config(ConvertTargetType.get_string(convert_type))
        if not self._enum_config:
            raise Exception('enum_generate_config not define')
        
    @property
    def _generate_path(self):
        target_path = self._enum_config.generate_path
        return target_path

    @property
    def _generate_namespace(self):
        return self._enum_config.namespace

    def generate(self, enum_meta_data:EnumMetaData):
        raise NotImplementedError('EnumGenerator not implement')

class CSharpEnumGenerator(EnumGenerator):
    '''
    C#용 Enum 생성
    '''

    def __init__(self, yaml_config:YamlConfig):
        super().__init__(yaml_config, ConvertTargetType.CSharp)
    
    def generate(self, enum_meta_data:EnumMetaData):

        target_path = self._generate_path
        namespace = self._generate_namespace

        try:
            if target_path.endswith('.cs') == False:
                raise Exception('target_path is not cs file')

            target_path = convert_path(target_path)
            mkdir_path(target_path)

            enum_content = ''

            # namespace begin
            if namespace:
                enum_content = 'namespace {0}\n'.format(namespace)
                enum_content += '{\n'

            prefix = '\t' if namespace else ''

            for enum_meta_info in enum_meta_data.enum_meta_infos:
                enum_unit:str = enum_meta_info.to_csharp()

                for line in enum_unit.splitlines():
                    enum_content += prefix + line + '\n'

            # namespace end
            if namespace:
                enum_content += '}\n'

            with open(target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

class DartEnumGenerator(EnumGenerator):
    '''
    Dart용 Enum 생성
    '''

    def __init__(self, yaml_config:YamlConfig):
        super().__init__(yaml_config, ConvertTargetType.Dart)

    def generate(self, enum_meta_data:EnumMetaData):

        target_path = self._generate_path

        try:
            if target_path.endswith('.dart') == False:
                raise Exception('target_path is not dart file')

            target_path = convert_path(target_path)
            mkdir_path(target_path)

            enum_content = ''
            for enum_meta_info in enum_meta_data.enum_meta_infos:
                enum_unit = enum_meta_info.to_dart()
                enum_content += enum_unit

            enum_content += '\n'
            enum_content += self.__generate_enum_get_index_func(enum_meta_data)

            with open(target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

    def __generate_enum_get_index_func(self, enum_meta_data:EnumMetaData):
        builder = ''
        builder += 'int getGenerateEnumIndex(dynamic value) {\n'

        for enum_meta_info in enum_meta_data.enum_meta_infos:
            builder += '\tif (value is {0}) {{\n'.format(enum_meta_info.enum_name)
            builder += '\t\treturn value.index;\n'
            builder += '\t}\n'

        builder += '\treturn 0;\n'
        builder += '}\n'

        return builder