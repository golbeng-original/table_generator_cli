import os
from ruamel.yaml import YAML, CommentToken

class EnumField:
    field_name = ''
    field_value = None
    field_comment = None

    def __str__(self):
        return '{0} = {1} //{2}'.format(self.field_name, self.field_value, self.field_comment)

class EnumMetaInfo:
    enum_name:str
    enum_fields:list

    def __str__(self):
        str_value = self.enum_name + '\n'
        for enum_field in self.enum_fields:
            str_value += '\t{0}\n'.format(enum_field)

        return str_value

    def is_exist_enum_field(self, enum_field_name:str):
        filtered = filter(lambda item : item.field_name.lower() == enum_field_name.lower(), self.enum_fields)
        return len(list(filtered)) > 0

    def to_csharp(self):
        enum_body = 'public enum {0}\n'.format(self.enum_name)
        enum_body += '{\n'

        enum_value = 0
        for field in self.enum_fields:

            if field.field_value is not None:
                enum_value = int(field.field_value)
            
            enum_field_str = '\t{0} = {1}'.format(field.field_name, enum_value)
            if field.field_comment is not None and len(field.field_comment) > 0:
                enum_field_str = enum_field_str + ', /// {0}\n'.format(field.field_comment)
            else:
                enum_field_str = enum_field_str + ',\n'
            
            

            enum_body += enum_field_str

            enum_value = enum_value + 1

        enum_body += '}\n'
        
        return enum_body

    def to_dart(self):
        enum_body = 'enum {0}\n'.format(self.enum_name)
        enum_body += '{\n'

        prev_enum_value = 0
        enum_value = 0
        for field in self.enum_fields:

            if field.field_value is not None:
                enum_value = int(field.field_value)

            # 중간에 건너뛰는 값은 임시 _{0}로 표시
            for empty_value in range(prev_enum_value, enum_value):
                empty_field_str = '\t_{0},\n'.format(empty_value)
                enum_body += empty_field_str
            
            enum_field_str = '\t{0}'.format(field.field_name.lower())
            if field.field_comment is not None and len(field.field_comment) > 0:
                enum_field_str = '\t/// {0}\n{1},\n'.format(field.field_comment,enum_field_str)
            else:
                enum_field_str = enum_field_str + ',\n'
            
            enum_body += enum_field_str

            enum_value = enum_value + 1
            prev_enum_value = enum_value

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

    def parsing(self, filepath):

        if os.path.exists(filepath) == False:
            raise FileNotFoundError('{filepath} is not found'.format(**locals()))

        if self.__check_yaml_file(filepath) == False:
            raise Exception('{filepath} is not .yaml'.format(**locals()))

        enum_meta_data = EnumMetaData()

        try:
            root = None
            with open(filepath, 'r') as f:
                yaml = YAML()
                root = yaml.load(f)

            for enum_key, enum_context in root.items():
                enum_meta_info = EnumMetaInfo()
                enum_meta_info.enum_name = enum_key
                enum_meta_info.enum_fields = self.__get_enum_values(enum_context)

                enum_meta_data.enum_meta_infos.append(enum_meta_info)

            return enum_meta_data

        except Exception as e:
            raise Exception('{filepath} load error [{e}]'.format(**locals()))

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

        return enum_fields
