#import yaml
import generate
import re
from ruamel.yaml import YAML, CommentToken

from parser.schema_table_parser import ExcelSchemaParser, ExcelSchemaData
from parser.data_table_parser import ExcelDataParser
from parser.enum_define_parser import EnumDefineParser

from generate.enum_generator import EnumGenerator
from generate.excel_format_sync_generator import ExcelFormatSyncGenerator

print('execute parser!!')

try:
    schema_parser = ExcelSchemaParser()
    excel_schema_data:ExcelSchemaData = schema_parser.parsing('./testFile/piadgoods.schema.xlsx')
    for field in excel_schema_data.get_fields():
        print('{0} => type : {1}'.format(field.name, field.get_nativetype()))

    data_parser = ExcelDataParser()
    excel_data = data_parser.parsing(excel_schema_data, './testFile/piadgoods.xlsx')

    for row in excel_data.get_column_mapping_rows():
        print(row)

    ## Enum 관련 처리 
    
    enum_parser = EnumDefineParser()
    enum_data = enum_parser.parsing('./testFile/enum_define.yaml')

    #for enum_meta in enum_data.enum_metas:
    #    print(enum_meta)

    enum_generate = EnumGenerator(enum_data)
    enum_generate.generate_csharp('./temp_generate/enum.cs')
    enum_generate.generate_dart('./temp_generate/enum.dart')

    syncGenerator = ExcelFormatSyncGenerator(enum_data, excel_schema_data)
    syncGenerator.new_excel_data('./temp_generate')

except Exception as e:
    print(e)



def csfile_paring_test():
    enumlist_regex = r'public enum .+?}'
    enumcontext_regex = r'public enum (?P<enum_name>.+?)\s?{(?P<enum_context>.+?)}'

    filepath = '/Volumes/workspace/ing_project/CookieProject/Common/CommonPackage/src/enum/Enums.cs'

    with open(filepath, 'r') as filecontext:
        context_match = filecontext.read()
        context_match = context_match.replace('\r', '')
        context_match = context_match.replace('\n', '')
        context_match = context_match.replace('\t', '')


        # enum 목록 찾기
        enum_list = re.findall(enumlist_regex, context_match, re.I)
        print(len(enum_list))
        for enum in enum_list:

            match = re.match(enumcontext_regex, enum, re.I)
            if match is None:
                continue;

            enum_name = match.group('enum_name')
            enum_context = match.group('enum_context')

            enum_items = enum_context.split(',')
            for enum_item in enum_items:
                enum_item = enum_item.strip()
                if len(enum_item) == 0:
                    continue
                
                item_regexp = r'\[Description\(\"(.+)\"\)\](\S+?)\s?=?\s?([0-9]+)?),?'
                item_regexp = r'\[Description\(\"(?P<description>.+?)\"\)\](?P<item>\S+)\s?=?\s?(?P<value>[0-9]+)?'
                context_match = re.match(item_regexp, enum_item, re.I)

                if context_match is None:
                    print('{0} - fail'.format(enum_item))
                    continue

                enum_value = context_match.group('value')
                print(context_match.group('description'), ' - ', context_match.group('item'), ' - ', enum_value)

            break

def get_yaml_next_value(y):
    with open('./testfile/enum_define.yaml', 'r') as f:

        yaml = YAML()
        root = yaml.load(f)

        for root_key in root:

            # root_key is enum name
            enum_context = root[root_key]

            for enum_item in enum_context:

                if isinstance(enum_item, dict):

                    # enum_item_key, enum_item_value
                    for enum_item_key, enum_item_value in enum_item.items():
                        print(enum_item_key)
                        print(enum_item_value)

                    items = enum_item.ca.items
                    for _, value in items.items():
                        commentToken = [comment for comment in value if isinstance(comment, CommentToken)]
                        if len(commentToken) == 0:
                            break;

                        c:CommentToken = commentToken[0]
                        print(c.value)
                        break;


    
    #if y.ca.comment is not None:

    #yaml_test = yaml.load_all(f, Loader=yaml.UnsafeLoader)
    #yaml_test = yaml.load(f)

    #for y in yaml_test:
    #    print(y)

    #print(yaml_test)


"""
write_wb = Workbook()

write_ws = write_wb.create_sheet('new Sheet')

write_ws = write_wb.active
write_ws['A1'] = '숫자'

write_ws.append([1,2,3])

os.mkdir('./temp')

write_wb.save('./temp/python_excel.xlsx')
"""

