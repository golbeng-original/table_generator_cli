#import yaml
import generate
import re
import numpy
from io import StringIO
from ruamel.yaml import YAML, CommentToken

from config import YamlConfig, YamlObject

from parser.schema_table_parser import ExcelSchemaParser, ExcelSchemaData
from parser.data_table_parser import ExcelDataParser
from parser.enum_define_parser import EnumDefineParser

from generate.enum_generator import CSharpEnumGenerator, DartEnumGenerator
from generate.excel_format_sync_generator import ExcelFormatSyncGenerator

#
from generate.excel_schema_class_genertor import CSharpSchemaClassConverter, DartSchemaClassConverter

print('execute parser!!')

global_config = YamlConfig('./testfile/generate.config.yaml')

try:
    
    ## 파일 생성 관련 기본 데이터 읽어오기 ##################

    # Enum 정의 파일 Config로 부터 읽어오기
    enum_define_path = global_config.get_value('enum_generate_config.enum_define_path')
    
    enum_parser = EnumDefineParser()
    enum_data = enum_parser.parsing(enum_define_path)
    #for enum_meta in enum_data.enum_metas:
    #    print(enum_meta)

    # Schema 파일 읽어오기
    schema_parser = ExcelSchemaParser()
    excel_schema_data:ExcelSchemaData = schema_parser.parsing('./testFile/piadgoods.schema.xlsx')
    #for field in excel_schema_data.get_fields():
    #    print('{0} => type : {1}'.format(field.name, field.get_nativetype()))

    # ExcelData 읽어오기 (schemaParser랑 매칭 시켜야 한다..)
    data_parser = ExcelDataParser()
    excel_data = data_parser.parsing(excel_schema_data, './testFile/piadgoods.xlsx')
    #for row in excel_data.get_column_mapping_rows():
    #    print(row)

    #################################################

    ## enumData로 각 언어로 enum 생성 ##################
    # csharp namespace 가져오기
    csharp_namespace = global_config.get_value('enum_generate_config.csharp.namespace')

    # Enum Parser -> csharp Generator로... 
    cshap_enum_generator = CSharpEnumGenerator(enum_data, csharp_namespace)
    
    # csharp 저장 대상 파일 경로에 Enum 파일 생성하기 
    csharp_genrate_path = global_config.get_value('enum_generate_config.csharp.generate_path')
    cshap_enum_generator.generate(csharp_genrate_path)

    # Enum Parser -> dart Generator로...
    dart_enum_generator = DartEnumGenerator(enum_data)

    # dart 저장 대상 파일 경로에 Enum 파일 생성하기
    dart_genrate_path = global_config.get_value('enum_generate_config.dart.generate_path')
    dart_enum_generator.generate(dart_genrate_path)

    ##########################################################

    ## schema로 부터 Data Excel 처리 ###########################

    # schema (feat. enumdata) 정보로 부터 새 Data Excel 파일 생성
    #syncGenerator = ExcelFormatSyncGenerator(enum_data, excel_schema_data)
    #syncGenerator.new_excel_data('./temp_generate')
    
    # schema (feat. ecnumdata) 정보로 부터 기존 Data Excel Schmea 포맷 맞추기
    syncGenerator = ExcelFormatSyncGenerator(enum_data, excel_schema_data)
    syncGenerator.format_sync('./temp_generate/piadgoods.xlsx')

    #######################################################################

    ## schema로 부터 각 언어 Class 생성 #######################################
    ## 모든 schema 각 언어 class로 생성 후 한 파일에 써야한다. #####################

    #class_generator = CSharpSchemaClassConverter(excel_schema_data, enum_data)
    #print(class_generator.generate())
    #print(class_generator.generate_meta())

    class_generator = DartSchemaClassConverter(excel_schema_data, enum_data)
    print(class_generator.generate())

    print(class_generator.generate_meta())

    #######################################################################

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

