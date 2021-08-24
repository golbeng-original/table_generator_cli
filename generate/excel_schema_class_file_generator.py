import os
import threading
import time
import math

from enum import Enum
from io import FileIO

from parser.schema_table_parser import ExcelSchemaParser, ExcelSchemaData
from parser.enum_define_parser import EnumMetaData
from generate.generate_struct import ConvertTargetType
from generate.excel_schema_class_convert import CSharpSchemaClassConverter
from generate.excel_schema_class_convert import DartSchemaClassConverter

from core.yaml_config import YamlConfig, GenerateYamlObject
from core.path_util import mkdir_path, convert_path
from core.progress_woker import ProgressWorker


class ExcelSchemaClassFileGenerator:
    _generate_config:GenerateYamlObject = None

    def __init__(self, yaml_config:YamlConfig, convert_type:ConvertTargetType, configure_path:str = 'class_generate_config'):

        convert_type_str:str = ConvertTargetType.get_string(convert_type)
        self._generate_config = yaml_config.get_class_generate_config(convert_type_str, configure_path)

        if not self._generate_config:
            raise Exception('get generate_config failed')

        if not self._generate_config.class_generate_path:
            raise Exception('class generate path not define')

        if not self._generate_config.meta_generate_path:
            raise Exception('meta generate path not define')

    def generate(self, generate_list:list, enum_data:EnumMetaData):

        #
        generate_path = convert_path(self._generate_config.class_generate_path)
        mkdir_path(generate_path)

        meta_generate_path = convert_path(self._generate_config.meta_generate_path)
        mkdir_path(meta_generate_path)

        #
        worker = ProgressWorker(self.__generate_worker(generate_list, generate_path, meta_generate_path, enum_data, self._generate_config))
        worker.start()

        return worker

    def __generate_worker(self, generate_list:list, generate_path:str, meta_generate_path:str, enum_meta:EnumMetaData, generate_config:GenerateYamlObject):

        def work(worker):
            # class Generate
            try:
                self._inner_genrate_prepare(worker, generate_list, enum_meta, generate_config)
                self.__generate_class(worker, generate_path, generate_list, generate_config)
                self.__generate_meta(worker, meta_generate_path, generate_list, generate_config)
            except:
                raise 

        return work
        
    def __generate_class(self, worker:ProgressWorker, generate_path:str, generate_list:list, generate_config:GenerateYamlObject):
        
        if os.path.exists(generate_path):
            os.remove(generate_path)

        try:
            with open(generate_path, 'w') as f:
                self._inner_generate_class(worker, f, generate_list, generate_config)

        except Exception as e:
            raise e

    def __generate_meta(self, worker:ProgressWorker, generate_path:str, generate_list:list, generate_config:GenerateYamlObject):
        if os.path.exists(generate_path):
            os.remove(generate_path)

        try:
            with open(generate_path, 'w') as f:
                self._inner_generate_meta(worker, f, generate_list, generate_config)

            return True

        except Exception as e:
            raise e

    def _inner_genrate_prepare(self, worker:ProgressWorker, generate_list:list, enum_meta:EnumMetaData, generate_config:GenerateYamlObject):
        pass

    def _inner_generate_class(self, worker:ProgressWorker, file:FileIO, generate_list:list, generate_config:GenerateYamlObject):
        raise NotImplementedError('need implement _inner_generate_class')

    def _inner_generate_meta(self, worker:ProgressWorker, file:FileIO, generate_list:list, generate_config:GenerateYamlObject):
        raise NotImplementedError('need implement _inner_generate_meta')

class PrepareSchemaClassFileGenerator(ExcelSchemaClassFileGenerator):
    __schema_mapping = {}

    def __init__(self, yaml_config:YamlConfig, convert_type:ConvertTargetType):
        super().__init__(yaml_config, convert_type)

    def _find_converter(self,schema_file:str):
        if schema_file not in self.__schema_mapping:
            return None

        return self.__schema_mapping[schema_file]

    def _inner_genrate_prepare(self, worker:ProgressWorker, generate_list:list, enum_meta:EnumMetaData, generate_config:GenerateYamlObject):

        total_count = len(generate_list)
        for idx, generate_schema_file in enumerate(generate_list):

            filename = os.path.basename(generate_schema_file)

            curr_progress = (float(idx+1) / float(total_count)) * 100
            curr_progress = min(curr_progress, 100)
            worker.updateProgress(curr_progress, "\"{0}\" parsing...".format(filename))

            # Schema 
            schema_parser = ExcelSchemaParser(generate_schema_file)
            excel_schema_data:ExcelSchemaData = schema_parser.parsing_sync(enum_meta)

            self.__schema_mapping[generate_schema_file] = excel_schema_data


class CSharpSchemaClassFileGenerator(PrepareSchemaClassFileGenerator):
    
    def __init__(self, yaml_config:YamlConfig):
        super().__init__(yaml_config, ConvertTargetType.CSharp)
    
    def _inner_generate_class(self, worker: ProgressWorker, file: FileIO, generate_list: list, generate_config: GenerateYamlObject):
        
        using_list = generate_config.class_generate_usings
        namespace = generate_config.namespace
        db_extension = generate_config.db_extension

        # using
        if using_list:
            for using in using_list:
                file.write('using {0};\n'.format(using))

            file.write('\n')

        # namespace
        if namespace:
            file.write('namespace {0}\n'.format(namespace))
            file.write('{\n')

        prefix = '\t' if namespace else ''

        # class write
        total_count = len(generate_list)
        for idx, generate_file in enumerate(generate_list):

            filename = os.path.basename(generate_file)

            curr_progress = (float(idx) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 50))
            worker.updateProgress(curr_progress, "[c#]\"{0}\" convert class ".format(filename))

            schema_data = self._find_converter(generate_file)

            # Schema 
            schema_class_convert = CSharpSchemaClassConverter(schema_data, db_extension)
            schema_class = schema_class_convert.generate()

            for line in schema_class.splitlines():
                file.write(prefix + line + '\n')

            curr_progress = (float(idx + 1) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 50))
            worker.updateProgress(curr_progress, "[c#]\"{0}\" complete".format(filename))

        # namepsace end
        if namespace:
            file.write('}\n')


    def _inner_generate_meta(self, worker: ProgressWorker, file: FileIO, generate_list: list, generate_config: GenerateYamlObject):

        meta_collection = generate_config.meta_collection

        using_list = generate_config.meta_generate_usings
        namespace = generate_config.namespace
        db_extension = generate_config.db_extension

        entry_class, entry_name = generate_config.meta_entry_info

        if using_list:
            for using in using_list:
                file.write('using {0};\n'.format(using))

            file.write('\n')

        # namespace
        if namespace:
            file.write('namespace {0}\n'.format(namespace))
            file.write('{\n')

        global_prefix = '\t' if namespace else ''

        # entry point
        file.write(global_prefix + 'public partial class {0}\n'.format(entry_class))
        file.write(global_prefix + '{\n')

        file.write(global_prefix + '\tprivate static void {0}()\n'.format(entry_name))
        file.write(global_prefix + '\t{\n')

        prefix = '\t\t' if namespace else '\t'
        prefix = global_prefix + prefix
        
        total_count = len(generate_list)
        # meta write
        for idx, generate_file in enumerate(generate_list):

            filename = os.path.basename(generate_file)

            curr_progress = 50 + (float(idx) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 100))
            worker.updateProgress(curr_progress, "[c#]\"{0}\" convert meta".format(filename))

            schema_data = self._find_converter(generate_file)

            # Schema 
            schema_class_convert = CSharpSchemaClassConverter(schema_data, db_extension)
            schema_class = schema_class_convert.generate_meta(meta_collection)

            for line in schema_class.splitlines():
                file.write(prefix + line + '\n')

            curr_progress = 50 + (float(idx + 1) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 100))
            worker.updateProgress(curr_progress, "[c#]\"{0}\" complete".format(filename))

        # entry poinr end
        file.write(global_prefix + '\t}\n')
        file.write(global_prefix + '}\n')

        # namepsace end
        if namespace:
            file.write('}\n')


class DartSchemaClassFileGenerator(PrepareSchemaClassFileGenerator):
    
    def __init__(self, yaml_config:YamlConfig):
        super().__init__(yaml_config, ConvertTargetType.Dart)

    def _inner_generate_class(self, worker: ProgressWorker, file: FileIO, generate_list: list, generate_config: GenerateYamlObject):
        import_list = generate_config.class_generate_imports
        db_extension = generate_config.db_extension

        # using
        if import_list:
            for import_element in import_list:
                file.write('import \'{0}\';\n'.format(import_element))

            file.write('\n')

        # class write
        total_count = len(generate_list)
        for idx, generate_file in enumerate(generate_list):

            filename = os.path.basename(generate_file)

            curr_progress = (float(idx) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 50))
            worker.updateProgress(curr_progress, "[dart]\"{0}\" convert class ".format(filename))

            schema_data = self._find_converter(generate_file)

            # Schema 
            schema_class_convert = DartSchemaClassConverter(schema_data, db_extension)
            schema_class = schema_class_convert.generate()

            for line in schema_class.splitlines():
                file.write(line + '\n')

            curr_progress = (float(idx + 1) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 50))
            worker.updateProgress(curr_progress, "[dart]\"{0}\" complete".format(filename))


    def _inner_generate_meta(self, worker: ProgressWorker, file: FileIO, generate_list: list, generate_config: GenerateYamlObject):
        
        meta_collection = generate_config.meta_collection
        
        import_list = generate_config.meta_generate_imports
        namespace = generate_config.namespace
        db_extension = generate_config.db_extension

        _, entry_name = generate_config.meta_entry_info

        if import_list:
            for import_element in import_list:
                file.write('import \'{0}\';\n'.format(import_element))

            file.write('\n')

        # entry point
        file.write('void {0}()\n'.format(entry_name))
        file.write('{\n')

        total_count = len(generate_list)
        # meta write
        for idx, generate_file in enumerate(generate_list):

            filename = os.path.basename(generate_file)

            curr_progress = 50 + (float(idx) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 100))
            worker.updateProgress(curr_progress, "[dart]\"{0}\" convert meta".format(filename))

            schema_data = self._find_converter(generate_file)

            # Schema 
            schema_class_convert = DartSchemaClassConverter(schema_data, db_extension)
            schema_class = schema_class_convert.generate_meta(meta_collection)

            for line in schema_class.splitlines():
                file.write('\t\t' + line + '\n')

            curr_progress = 50 + (float(idx + 1) / float(total_count)) * 50
            curr_progress = int(min(curr_progress, 100))
            worker.updateProgress(curr_progress, "[dart]\"{0}\" complete".format(filename))

        # entry poinr end
        file.write('}\n')

        # namepsace end
        if namespace:
            file.write('}\n')
