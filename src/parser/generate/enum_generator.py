import os
from parser.enum_define_parser import EnumMetaData

class EnumGenerator:
    enum_meta_data:EnumMetaData = None

    def __init__(self, enum_meta_data:EnumMetaData):
        self.enum_meta_data = enum_meta_data

    # c# 타겟 생성
    def generate_csharp(self, target_path:str, namespace = ''):
        try:
            
            if target_path.endswith('.cs') == False:
                raise Exception('target_path is not cs file')

            absolute_target_path = os.path.abspath(target_path)
            dirs = os.path.dirname(absolute_target_path)
            os.makedirs(dirs, exist_ok=True)

            enum_content = '';
            if len(namespace) > 0:
                enum_content = 'namespace {0}\n'.format(namespace)
                enum_content += '{\n'

            for enum_meta_info in self.enum_meta_data.enum_metas:
                enum_unit = enum_meta_info.to_csharp()

                enum_content += enum_unit

            if len(namespace) > 0:
                enum_content += '}\n'

            with open(absolute_target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

    # dart target 생성
    def generate_dart(self, target_path):
        try:
            if target_path.endswith('.dart') == False:
                raise Exception('target_path is not dart file')

            absolute_target_path = os.path.abspath(target_path)
            dirs = os.path.dirname(absolute_target_path)
            os.makedirs(dirs, exist_ok=True)

            enum_content = ''
            for enum_meta_info in self.enum_meta_data.enum_metas:
                enum_unit = enum_meta_info.to_dart()

                enum_content += enum_unit

            with open(absolute_target_path, 'w') as f:
                f.write(enum_content)

        except:
            raise

    # 다른 언어 생성
    def generate_etc(self, target_path):
        pass