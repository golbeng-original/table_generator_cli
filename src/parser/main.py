import os
import re
import click

from generate.generate_struct import ConvertTargetType
from core.progress_woker import ProgressWorker

from core.yaml_config import YamlConfig
from core.path_util import register_path_enviorment, convert_path, find_glob_files, find_identity_dataname

from parser.schema_table_parser import ExcelSchemaParser, ExcelSchemaData
from parser.data_table_parser import ExcelData, ExcelDataParser
from parser.enum_define_parser import EnumDefineParser

from generate.enum_generator import CSharpEnumGenerator, DartEnumGenerator
from generate.excel_format_sync_generator import ExcelFormatSyncGenerator
from generate.excel_schema_class_file_generator import CSharpSchemaClassFileGenerator
from generate.excel_schema_class_file_generator import DartSchemaClassFileGenerator

from generate.excel_data_generator import ExcelDataGenerator

def do_worker_output(is_json, worker:ProgressWorker):

    if is_json:
        worker.get_progress_json_printer().output()
    else:
        worker.get_progress_conosle_printer().output()

    if worker.error:
        raise Exception(worker.error)

@click.group()
@click.option('--config', type=str)
@click.option('--workspace', type=str)
@click.option('--json', count=True)
@click.pass_context
def cli(ctx, config:str, workspace:str, json):

    if not workspace:
        click.echo('need input --workspace=<workspace path>', color=True)
        exit(1)

    workspace = workspace.strip('"')
    workspace = workspace.strip()
    workspace = convert_path(workspace)
    if not os.path.exists(workspace):
        click.echo('workspace not found', color=True)
        exit(1)
    
    if not config:
        click.echo('need input --config=<config path>', color=True)
        exit(1)

    register_path_enviorment('workspace', workspace)

    #
    config = config.strip('"')
    config = config.strip()
    config = convert_path(config)

    if not os.path.exists(config):
        click.echo('config file not found', color=True)
        exit(1)
    
    try:
        global_config = YamlConfig(config)
        ctx.obj['config'] = global_config
    except Exception as e:
        click.echo(f'[exception] {e}')
        exit(1)

    ctx.obj['json'] = True if json else False


# enum 파일 생성 Command
@cli.command()
@click.option('--dart', count=True)
@click.option('--csharp', count=True)
@click.option('--help', count=True)
@click.pass_context
def enum_generate(ctx, dart, csharp, help):

    if help:
        click.echo('enum meta file을 이용하여 (dart, csharp) 타겟 enum class들을 생성 해 준다.')
        click.echo('OPTIONS')
        click.echo('\t--dart : dart language project target db create')
        click.echo('\t--csharp : csharp language project target db create')
        exit(0)

    global_config:YamlConfig = ctx.obj['config']

    if not dart and not csharp:
        click.echo('need input --dart or --csharp')
        exit(1)

    try:
        enum_parser = EnumDefineParser(global_config)
        enum_data = enum_parser.parsing()

        ## dart 타겟으로 enum 파일 생성
        if dart:
            dart_enum_generator = DartEnumGenerator(global_config)
            dart_enum_generator.generate(enum_data)

        # csharp 타겟으로 enum 파일 생성
        if csharp:
            csharp_enum_generator = CSharpEnumGenerator(global_config)
            csharp_enum_generator.generate(enum_data)
    
    except Exception as e:
        click.echo(f'[excpetion] {e}')
        exit(1)

# schema class 생성 command
@cli.command()
@click.option('--dart', count=True)
@click.option('--csharp', count=True)
@click.option('--help', count=True)
@click.pass_context
def class_generate(ctx, dart, csharp, help):

    if help:
        click.echo('schema들을 (dart, csharp) 타겟 DAO class들을 생성 해 준다.')
        click.echo('OPTIONS')
        click.echo('\t--dart : dart language project target db create')
        click.echo('\t--csharp : csharp language project target db create')
        exit(0)

    global_config:YamlConfig = ctx.obj['config']
    output_json = ctx.obj['json']

    if not dart and not csharp:
        click.echo('need input --dart or --csharp')
        exit(1)

    collection_config = global_config.get_collection_config()

    schema_list = find_glob_files(collection_config.schema_file_glob)
    if not schema_list:
        click.echo('schema list is empty')
        exit(1)

    try:

        enum_parser = EnumDefineParser(global_config)
        enum_data = enum_parser.parsing()

        if dart:
            dart_class_generator = DartSchemaClassFileGenerator(global_config)
            worker = dart_class_generator.generate(schema_list, enum_data)
        
            do_worker_output(output_json, worker)

        if csharp:
            csharp_class_generator = CSharpSchemaClassFileGenerator(global_config)
            worker = csharp_class_generator.generate(schema_list, enum_data)
        
            do_worker_output(output_json, worker)
    
    except Exception as e:
        click.echo(f'[exception] {e}')
        exit(1)


# shcema에 해당하는 data db로 생성 command
@cli.command()
@click.option('--dart', count=True)
@click.option('--csharp', count=True)
@click.option('--schema', type=str)
@click.option('--help', count=True)
@click.pass_context
def data_generate(ctx, dart, csharp, schema, help):

    if help:
        click.echo('schema에 해당하는 data Excel 파일 수집 후 db 생성')
        click.echo('OPTIONS')
        click.echo('\t--schema=<exist schema name>')
        click.echo('\t--dart : dart language project target db create')
        click.echo('\t--csharp : csharp language project target db create')
        exit(0)

    global_config:YamlConfig = ctx.obj['config']
    output_json = ctx.obj['json']

    if not dart and not csharp:
        click.echo('need input --dart or --csharp')
        exit(1)
    
    if not schema:
        click.echo('need input --schema=<schema name>')
        exit(1)

    # schema에 해당하는 .schema.xlsx 찾아야 한다.
    # schema에 해당하는 .data.xlsx 찾아야 한다.

    collection_config = global_config.get_collection_config()

    schema_path_list:list = find_glob_files(collection_config.schema_file_glob, schema=schema)
    data_path_list:list = find_glob_files(collection_config.data_file_glob, schema=schema)

    if not len(schema_path_list):
        click.echo(f'{schema} schema.xlsx not exists')
        exit(1)

    if not len(data_path_list):
        click.echo(f'{schema} data.xlsx not exists')
        exit(1)

    try:
        # enum Data 가져오기
        enum_parser = EnumDefineParser(global_config)
        enum_data = enum_parser.parsing()

        #schema Data 가져오기
        schema_file = schema_path_list[0]
        schema_parser = ExcelSchemaParser(schema_file)
        worker:ProgressWorker = schema_parser.parsing_async(enum_data)
        do_worker_output(output_json, worker)

        schema_data:ExcelSchemaData = worker.result

        # data 가져오기
        excel_data:ExcelData = None
        for data_path in data_path_list:

            data_parser = ExcelDataParser(data_path, is_convert_sql_value=True)
            worker = data_parser.parsing_async(schema_data, enum_data)

            do_worker_output(output_json, worker)

            if not excel_data:
                excel_data = worker.result
            else:
                excel_data.merge(worker.result)

        # data -> db로 만둘기
        if dart:
            data_generator = ExcelDataGenerator(global_config, ConvertTargetType.Dart)    
            worker = data_generator.generate_async(excel_data)

            do_worker_output(output_json, worker)

        if csharp:
            csharp_generator = ExcelDataGenerator(global_config, ConvertTargetType.CSharp)    
            worker = csharp_generator.generate_async(excel_data)

            do_worker_output(output_json, worker)

    except Exception as e:
        click.echo(f'[exception] {e}')
        exit(1)

#schema와 data xlsx schema 동기화
@cli.command()
@click.option('--schema', type=str)
@click.pass_context
def schema_sync(ctx, schema, help):

    if help:
        click.echo('schema와 기존에 schema와 연동되는 기존 데이터와 포맷 동기화 한다.')
        click.echo('OPTIONS')
        click.echo('\t--schema=<exist schema name>')
        exit(0)

    global_config:YamlConfig = ctx.obj['config']
    output_json = ctx.obj['json']

    if not schema:
        click.echo('need input --schema=<schema name>')
        exit(1)

    # schema에 해당하는 .schema.xlsx 찾아야 한다.
    # schema에 해당하는 .data.xlsx 찾아야 한다.

    collection_config = global_config.get_collection_config()

    schema_path_list:list = find_glob_files(collection_config.schema_file_glob, schema=schema)
    data_path_list:list = find_glob_files(collection_config.data_file_glob, schema=schema)

    if not len(schema_path_list):
        click.echo(f'{schema} schema.xlsx not exists')
        exit(1)

    if not len(data_path_list):
        click.echo(f'{schema} data.xlsx not exists')
        exit(1)

    try:

        # enum Data 가져오기
        enum_parser = EnumDefineParser(global_config)
        enum_data = enum_parser.parsing()

        #schema Data 가져오기
        schema_file = schema_path_list[0]
        schema_parser = ExcelSchemaParser(schema_file)
        worker:ProgressWorker = schema_parser.parsing_async(enum_data)
        
        do_worker_output(output_json, worker)

        schema_data:ExcelSchemaData = worker.result

        # 기존에 있던 데이터 
        for data_path in data_path_list:
            syncGenerator = ExcelFormatSyncGenerator(enum_data, schema_data)
            worker:ProgressWorker = syncGenerator.format_sync_async(data_path)

            do_worker_output(output_json, worker)

    except Exception as e:
        click.echo(f'[exception] {e}')
        exit(1)


#schema에 대한 data xlsx 파일 생성
@cli.command()
@click.option('--schema', type=str)
@click.option('--identity', type=str, default='')
@click.option('--help', count=True)
@click.pass_context
def schema_new_data(ctx, schema:str, identity:str, help):

    if help:
        click.echo('schema에 맞는 새로운 DataExcel 파일을 생성한다.')
        click.echo('OPTIONS')
        click.echo('\t--schema=<exist schema name>')
        click.echo('\t--identity=<data identity name>')
        exit(0)

    global_config:YamlConfig = ctx.obj['config']
    output_json = ctx.obj['json']

    if not schema:
        click.echo('need input --schema=<schema name>')
        exit(1)

    if not re.match(r'[0-9A-Za-z]?', identity):
        click.echo('--identity=name rule error [allow Alphabet or number]')
        exit(1)

    # schema에 해당하는 .schema.xlsx 찾아야 한다.
    # schema에 해당하는 .data.xlsx 찾아야 한다.

    collection_config = global_config.get_collection_config()

    schema_path_list:list = find_glob_files(collection_config.schema_file_glob, schema=schema)
    data_path_list:list = find_glob_files(collection_config.data_file_glob, schema=schema)

    try:
        # schema 파일이 있나?
        if not schema_path_list:
            raise Exception(f'schema xlsx not exists')
        
        # 기존에 이미 파일이 있나??
        for data_path in data_path_list:

            data_identity = find_identity_dataname(data_path)
            if data_identity.lower() == identity.lower():
                raise Exception(f'exist data identity [{data_path}]')

        # 새로 생성할 경로 가져오기
        new_data_fullpath = convert_path(collection_config.data_file_glob)
        
        new_data_dir_path = os.path.dirname(new_data_fullpath)
        
        join_list = [schema]
        if identity:
            join_list.append(identity)
        
        new_data_path = os.path.basename(new_data_fullpath)
        new_data_path = new_data_path.replace('*', '.'.join(join_list))

        new_data_fullpath = os.path.join(new_data_dir_path, new_data_path)

        # enum Data 가져오기
        enum_parser = EnumDefineParser(global_config)
        enum_data = enum_parser.parsing()

        #schema Data 가져오기
        schema_file = schema_path_list[0]
        schema_parser = ExcelSchemaParser(schema_file)
        worker:ProgressWorker = schema_parser.parsing_async(enum_data)
        
        do_worker_output(output_json, worker)

        schema_data:ExcelSchemaData = worker.result

        # data xlsx 생성
        syncGenerator = ExcelFormatSyncGenerator(enum_data, schema_data)
        worker:ProgressWorker = syncGenerator.new_excel_data_async(new_data_fullpath)
        
        do_worker_output(output_json, worker)

    except Exception as e:
        click.echo(f'[exception] {e}')
        exit(1)


if __name__ == '__main__':
    cli(obj={})
