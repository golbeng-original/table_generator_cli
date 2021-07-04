from openpyxl.descriptors import base
import generate
import os

from enum import Enum
from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from parser.enum_define_parser import EnumMetaData, EnumMetaInfo
from parser.schema_table_parser import ExcelSchemaData, ExcelSchemaField

class ExcelFormatSyncGenerator:

    enum_data:EnumMetaData = None
    schema_data:ExcelSchemaData = None

    __workbook:Workbook = None
    __data_worksheet:Worksheet = None

    __enum_cell_range = {}

    def __init__(self, enum_data:EnumMetaData, schema_data:ExcelSchemaData):
        self.enum_data = enum_data
        self.schema_data = schema_data
    
    def format_sync(self, target_excel_data_path:str):
        
        if target_excel_data_path.endswith('.xlsx') == False:
            raise Exception('{0} is not .xlsx file'.format(target_excel_data_path))

        absoulte_path = os.path.abspath(target_excel_data_path)
        dirs = os.path.dirname(absoulte_path)
        os.makedirs(dirs, exist_ok=True)

        if os.path.exists(absoulte_path) == False:
            raise Exception('{0} is not found'.format(target_excel_data_path))


        # enum worksheet부터 생성하자...
        self.__generate_enum_worksheet(self.enum_data, self.schema_data)



    def new_excel_data(self, target_directory_path:str):

        if os.path.isdir(target_directory_path) == False:
            raise Exception('{0} is not directory'.format(target_directory_path))
        
        absoulte_path = os.path.abspath(target_directory_path)
        dirs = os.path.dirname(absoulte_path)
        os.makedirs(dirs, exist_ok=True)

        target_data_name = '{0}.xlsx'.format(self.schema_data.schema_name)
        absoulte_path = os.path.join(absoulte_path, target_data_name)

        self.__workbook = Workbook()
        try:

            # enum worksheet부터 생성하자...
            self.__generate_enum_worksheet(self.enum_data, self.schema_data)

           #self.__data_worksheet = self.__workbook.create_sheet('DATA')
        except Exception as e:
            print(e)
        finally:
            if self.__workbook is not None:
                self.__workbook.close()

    def __generate_enum_worksheet(self, enum_data:EnumMetaData, schema_data:ExcelSchemaData):
        if 'ENUM' in self.__workbook.sheetnames:
            self.__workbook.remove(self.__workbook['ENUM'])

        enum_worksheet = self.__workbook.create_sheet('ENUM')

        # Schema에서 사용되는 Enum 타입들 조사
        use_enum = {}
        for schema_field in schema_data.get_fields():
            if schema_field.get_nativetype() != Enum:
                continue
        
            if enum_data.exist_enum(schema_field.type) == False:
                raise Exception('enum \'{0}\' type \'{1}\' not found'.format(schema_field.name, schema_field.type))

            use_enum[schema_field.type] = enum_data.get_enum_meta_info(schema_field.type)

        use_enum_key_list = use_enum.keys()
        for idx, enum_key in enumerate(use_enum_key_list):
            
            # 1열에 Enum Name
            cell = enum_worksheet.cell(1, idx + 1)
            cell.value = enum_key

            # 2열 부터 Enum의 Value들
            enum_meta:EnumMetaInfo = use_enum[enum_key]
            for field_idx, enum_field in enumerate(enum_meta.enum_fields):
                cell = enum_worksheet.cell(2+field_idx, idx + 1)
                cell.value = enum_field.field_name

            startIndex:str = '${0}${1}'.format(chr(ord('A') + idx), 2)
            endIndex:str = '${0}${1}'.format(chr(ord('A') + idx), 2 + len(enum_meta.enum_fields))
            
            self.__enum_cell_range[enum_key] = (startIndex, endIndex)
        