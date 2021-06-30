import os
from ruamel.yaml import YAML, CommentToken

class EnumField:
    field_name = ''
    field_value = None
    field_comment = None

    def __str__(self):
        return '{0} : {1} [{2}]'.format(self.field_name, self.field_value, self.field_comment)


class EnumMetaInfo:
    enum_name:str
    enum_fields:list

    def __str__(self):
        str_value = self.enum_name + '\n'
        for enum_field in self.enum_fields:
            str_value += '\t{0}\n'.format(enum_field)

        return str_value


class EnumDefineParser:

    def parsing(self, filepath):

        if os.path.exists(filepath) == False:
            raise FileNotFoundError('{filepath} is not found'.format(**locals()))

        if self.__check_yaml_file(filepath) == False:
            raise Exception('{filepath} is not .yaml'.format(**locals()))

        enums = []

        try:
            with open(filepath, 'r') as f:
                
                yaml = YAML()
                root = yaml.load(f)

                for enum_key, enum_context in root.items():
                    enum_meta_info = EnumMetaInfo()
                    enum_meta_info.enum_name = enum_key
                    enum_meta_info.enum_fields = self.__get_enum_values(enum_context)

                    enums.append(enum_meta_info)

            return enums
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
                    break;

                enum_field.field_comment = commentToken[0].value
                enum_field.field_comment = enum_field.field_comment .replace('\r', '')
                enum_field.field_comment = enum_field.field_comment.replace('\n', '')
                enum_field.field_comment = enum_field.field_comment .replace('\t', '')

                comment_start_char_index = enum_field.field_comment.find('#')
                enum_field.field_comment = enum_field.field_comment[comment_start_char_index:]

            enum_fields.append(enum_field)

        return enum_fields
