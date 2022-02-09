from core import progress_woker
from core.progress_woker import ProgressWorker
import os
import sqlite3

from parser.data_table_parser import ExcelData
from parser.schema_table_parser import ExcelSchemaData, ExcelSchemaField
from generate.generate_struct import ConvertTargetType
from core.path_util import convert_path, mkdir_path

class ExcelDataSqliteGenerator:

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
                conn = sqlite3.connect(outpath)

                if worker: worker.updateProgress(10, f'[{outpath}] {schema_data.table_name} table drop...')

                # 기존에 있던 Table들 삭제
                self.__delete_all_table(conn)

                if worker: worker.updateProgress(20, f'[{outpath}] {schema_data.table_name} table create...')

                # 테이블 생성
                self.__create_table(conn, schema_data)

                if worker: worker.updateProgress(50, f'[{outpath}] {schema_data.table_name} data insert...')

                # Bluk Insert
                self.__insert_rows(conn, schema_data, excel_data)

                if worker: worker.updateProgress(100, f'[{outpath}] {schema_data.table_name} generate complete')

            except Exception as e:
                print(f'[exception]{e}')

            finally:
                conn.close()

        return work

    #
    def __delete_all_table(self, conn:sqlite3.Connection):

        query_tables = 'SELECT name FROM sqlite_master WHERE type = "table"'

        try:
            cursor = conn.execute(query_tables)
            rows = cursor.fetchall()
            cursor.close()
            cursor = None

            if not len(rows):
                return

            for row in rows:
                delete_table = f'DROP TABLE {row[0]}'
                conn.execute(delete_table) 

        except:
            raise
        finally:
            if cursor:
                cursor.close()

    def __create_table(self, conn:sqlite3.Connection, schema_data:ExcelSchemaData):
        
        table_name = schema_data.table_name

        create_db_builder = ''
        create_db_builder += f'CREATE TABLE IF NOT EXISTS {table_name} '
        create_db_builder += '('

        # Field들 정의
        for schema_field in schema_data.get_fields():
            schema_field:ExcelSchemaField = schema_field

            field_db_builder = f'{schema_field.name} {schema_field.get_sqlitetype()} NOT NULL, '
            create_db_builder += field_db_builder

        # Primary 정의
        primary_fields = list(filter(lambda s : s.primary is True, schema_data.get_fields()))
        if len(primary_fields):
            primary_db_builder = 'PRIMARY KEY('
            for idx, primary_field in enumerate(primary_fields):
                primary_db_builder += f'"{primary_field.name}"'

                if idx < len(primary_fields) - 1:
                    primary_db_builder += ','

            primary_db_builder += ')'

            create_db_builder += primary_db_builder

        create_db_builder += ')'

        conn.execute(create_db_builder)

    def __insert_rows(self, conn:sqlite3.Connection, schema_data:ExcelSchemaData, excel_data:ExcelData):
        
        table_name = schema_data.table_name

        try:
            cursor = conn.cursor()
            schema_fields = list(schema_data.get_fields())

            insert_query = f'INSERT INTO {table_name}('
            for idx, schema_field in enumerate(schema_fields):
                insert_query += schema_field.name
                if idx < len(schema_fields) - 1:
                    insert_query += ','

            insert_query += ') '
            insert_query += 'VALUES ('

            for idx, schema_field in enumerate(schema_fields):
                insert_query += '?'
                if idx < len(schema_fields) - 1:
                    insert_query += ','

            insert_query += ')'

            rows = list(excel_data.get_rows())

            cursor.executemany(insert_query, rows)
            conn.commit()

        except:
            raise
        finally:
            cursor.close()