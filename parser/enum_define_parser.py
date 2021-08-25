import os
from ruamel.yaml import YAML, CommentToken

from core.path_util import convert_path, find_glob_files
from core.yaml_config import YamlConfig, EnumYamlObject

class DuplicateError(Exception):
    pass

class EnumField:
    field_name = ''
    field_value = None
    field_comment = None

    def __str__(self):
        return '{0} = {1} //{2}'.format(self.field_name, self.field_value, self.field_comment)

class EnumMetaInfo:
    enum_name:str
    enum_fields:list #EnumField

    def __str__(self):
        str_value = self.enum_name + '\n'
        for enum_field in self.enum_fields:
            str_value += '\t{0}\n'.format(enum_field)

        return str_value

    def is_exist_enum_field(self, enum_field_name:str):
        filtered = filter(lambda item : item.field_name.lower() == enum_field_name.lower(), self.enum_fields)
        return len(list(filtered)) > 0

    def get_enum_field(self, enum_field_name:str) -> EnumField:
        filtered = list(filter(lambda item : item.field_name.lower() == enum_field_name.lower(), self.enum_fields))
        if not len(filtered):
            raise ValueError(f'not exist [{enum_field_name}] in {self.enum_name}')

        return filtered[0]

    def to_csharp(self):
        enum_body = 'public enum {0}\n'.format(self.enum_name)
        enum_body += '{\n'

        for field in self.enum_fields:

            enum_field_str = '\t{0} = {1}'.format(field.field_name, field.field_value)
            if field.field_comment is not None and len(field.field_comment) > 0:
                enum_field_str = enum_field_str + ', /// {0}\n'.format(field.field_comment)
            else:
                enum_field_str = enum_field_str + ',\n'
            
            enum_body += enum_field_str

        enum_body += '}\n'
        
        return enum_body

    def to_dart(self):
        enum_body = 'enum {0}\n'.format(self.enum_name)
        enum_body += '{\n'

        prev_enum_value = 0
        for field in self.enum_fields:

            # 중간에 건너뛰는 값은 임시 _{0}로 표시
            if field.field_value - prev_enum_value > 1:
                for empty_value in range(prev_enum_value, field.field_value - 1):
                    empty_field_str = '\t_{0},\n'.format(empty_value + 1)
                    enum_body += empty_field_str
            
            enum_field_str = '\t{0}'.format(field.field_name.lower())
            if field.field_comment is not None and len(field.field_comment) > 0:
                enum_field_str = '\t/// {0}\n{1},\n'.format(field.field_comment,enum_field_str)
            else:
                enum_field_str = enum_field_str + ',\n'
            
            enum_body += enum_field_str

            prev_enum_value = field.field_value

        enum_body += '}\n'
        
        return enum_body
    
    def to_excel_comment(self):
        enum_comment = ''

        enum_value = 0
        for field in self.enum_fields:

            if field.field_value is not None:
                enum_value = int(field.field_value)
            
            enum_field_str = '{0} = {1}'.format(field.field_name, enum_value)
            if field.field_comment is not None and len(field.field_comment) > 0:
                enum_field_str = enum_field_str + ', /// {0}\n'.format(field.field_comment)
            else:
                enum_field_str = enum_field_str + ',\n'
            
            enum_comment += enum_field_str
            enum_value = enum_value + 1

        return enum_comment

class EnumMetaData:
    enum_meta_infos = []; #EnumMetaInfo

    def is_exist_enum(self, enumname:str):
        if self.get_enum_meta_info(enumname) is None:
            return False
        return True

    def get_enum_meta_info(self, enumname:str) -> EnumMetaInfo:
        for enum_meta in self.enum_meta_infos:
            if enum_meta.enum_name.lower() == enumname.lower():
                return enum_meta

        return None

class EnumDefineParser:

    __define_file_paths:str = ''

    def __init__(self, yaml_config:YamlConfig):

        collection_config = yaml_config.get_collection_config()
        
        self.__define_file_paths = find_glob_files(collection_config.enum_define_file_glob)
        if not self.__define_file_paths:
            raise Exception('enum_generate_config.enum_define_path not define')

    def parsing(self):

        enum_meta_data = EnumMetaData()

        for define_file_path in self.__define_file_paths:

            try:
                enum_meta_infos = self.__parsing_unit(define_file_path)

                for enum_meta_info in enum_meta_infos:
                    enum_meta_info:EnumMetaInfo = enum_meta_info
                
                    if enum_meta_data.is_exist_enum(enum_meta_info.enum_name):
                        raise DuplicateError(f'{enum_meta_info.enum_name} is duplicate')

                    enum_meta_data.enum_meta_infos.append(enum_meta_info)
            
            # 이건 생성 자체를 하면 안된다.
            except DuplicateError as e:
                raise
            except Exception as e:
                print(e)

        return enum_meta_data

    def __parsing_unit(self, file_path:str):

        file_path = convert_path(file_path)

        if os.path.exists(file_path) == False:
            raise FileNotFoundError(f'{file_path} is not found')

        if self.__check_yaml_file(file_path) == False:
            raise Exception(f'{file_path} is not .yaml')

        if not os.path.getsize(file_path):
            raise Exception(f'{file_path} is empty')

        try:
            root = None
            with open(file_path, 'r') as f:
                yaml = YAML()
                root = yaml.load(f)

            enum_meta_infos = []

            # enum data 수집
            for enum_key, enum_context in root.items():
                enum_meta_info = EnumMetaInfo()
                enum_meta_info.enum_name = enum_key
                enum_meta_info.enum_fields = self.__get_enum_values(enum_context)

                enum_meta_infos.append(enum_meta_info)
                #enum_meta_data.enum_meta_infos.append(enum_meta_info)

            # enum value 가 안 겹치게 정상적인가??
            for enum_meta_info in enum_meta_infos:
                if self.__is_duplicate_enum_value(enum_meta_info):
                    raise Exception(f'{enum_meta_info.enum_name} is enum_value duplicate!!')

            return enum_meta_infos

        except Exception as e:
            raise Exception(f'{file_path} load error [{e}]')

    def __check_yaml_file(self, filepath):

        filename:str = os.path.basename(filepath)
        return True if filename.endswith('.yaml') else False

    def __get_enum_values(self, enum_context):
        
        enum_fields = []

        for enum_item in enum_context:
            if isinstance(enum_item, dict) == False:
                break
            
            enum_field = EnumField()

            for enum_item_key, enum_item_value in enum_item.items():
                enum_field.field_name = enum_item_key
                enum_field.field_value = enum_item_value
                break

            # 주석 정보 가져오기
            for _, value in enum_item.ca.items.items():
                commentToken = [comment for comment in value if isinstance(comment, CommentToken)]
                if len(commentToken) == 0:
                    break

                enum_field.field_comment = commentToken[0].value
                enum_field.field_comment = enum_field.field_comment.strip()
                enum_field.field_comment = enum_field.field_comment.replace('\r', '')
                enum_field.field_comment = enum_field.field_comment.replace('\n', '')
                enum_field.field_comment = enum_field.field_comment.replace('\t', '')

                comment_start_char_index = enum_field.field_comment.find('#')
                enum_field.field_comment = enum_field.field_comment[comment_start_char_index+1:]

                enum_field.field_comment = enum_field.field_comment.strip()

            enum_fields.append(enum_field)

        # enum field 값 생성 체크 하기
        latet_value = 0
        for enum_field in enum_fields:
            enum_field:EnumField = enum_field

            if enum_field.field_value is not None:
                latet_value = int(enum_field.field_value)

            enum_field.field_value = latet_value

            latet_value += 1

        return enum_fields

    def __is_duplicate_enum_value(self, enum_meta_info:EnumMetaInfo):

        # enum field 값 중복 체크
        check_map:dict = {}
        for enum_field in enum_meta_info.enum_fields:
            enum_field:EnumField = enum_field

            if not enum_field.field_value in check_map:
                check_map[enum_field.field_value] = 0

            check_map[enum_field.field_value] += 1

        fliterd = list(filter(lambda v : v > 1, check_map.values()))

        return True if len(fliterd) else False
