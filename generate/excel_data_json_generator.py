from core import progress_woker
from core.progress_woker import ProgressWorker
import os
import json

from parser.data_table_parser import ExcelData
from parser.schema_table_parser import ExcelSchemaData, ExcelSchemaField
from core.path_util import convert_path, mkdir_path

class ExcelDataJsonGenerator:
    
    __outpath:str = ''

    def __init__(self, outpath:str):
        self.__outpath = outpath

    def generate_async(self, excel_data:ExcelData):
        work = self.__generate(excel_data, self.__outpath)
        progress_woker = ProgressWorker(work)
        progress_woker.start()
        
        return progress_woker
    
    def generate_sync(self, excel_data:ExcelData):
        work = self.__generate(excel_data, self.__outpath)
        work(None)
        
    
    def __generate(self, excel_data:ExcelData, outpath:str):
    
        schema_data:ExcelSchemaData = excel_data.get_excel_schema_data()
        outpath = convert_path(outpath)
        
        directory, _ = os.path.split(outpath)
        mkdir_path(directory)

        def work(worker:ProgressWorker):
            try:
                if worker: worker.updateProgress(0, f'[{outpath}] {schema_data.table_name} json generate...')

                self.__generate_json(outpath, schema_data, excel_data)

                if worker: worker.updateProgress(100, f'[{outpath}] {schema_data.table_name} json generate complete')

            except Exception as e:
                print(f'[exception]{e}')

        return work

    def __generate_json(self, outpath:str, schema_data:ExcelSchemaData, excel_data:ExcelData):
        
        tabledata = {}
        
        schema = []
        for schema_fields in schema_data.get_fields():
            schema_fields:ExcelSchemaField = schema_fields
            
            schema.append(schema_fields.__dict__)
            
        tabledata['schema'] = schema
        
        data_list = []
        for row in excel_data.get_rows():
            
            data_row = {}
            for schema_fields in schema_data.get_fields():
                schema_fields:ExcelSchemaField = schema_fields
                
                column_index = excel_data.get_column_field_index(schema_fields.name)
                
                data_row[schema_fields.name.lower()] = row[column_index]
                
            data_list.append(data_row)
        
        tabledata['data'] = data_list

        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(tabledata, f, indent=4, ensure_ascii=False)