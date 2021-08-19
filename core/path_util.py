import os
import re
import glob
from sys import dont_write_bytecode

__enviroment = {}

def register_path_enviorment(key:str, value:str):
    __enviroment[key] = value

def convert_path(path:str):
    for key, value in __enviroment.items():
        regex = re.compile(r'(\$\{' + key + r'\})+')

        path = regex.sub(value, path)

    regex = re.compile(r'(\$\{.+?\})+')
    path = regex.sub('', path)

    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    
    return path

def mkdir_path(path:str):

    if os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        return

    # directory 인지?
    split_ext = os.path.splitext(path)
    if not split_ext[1]:
        os.makedirs(path, exist_ok=True)
        return

    #os.path.splitext()

    dir = os.path.dirname(path)
    os.makedirs(dir, exist_ok=True)

def find_files(path:str):
    
    path = convert_path(path)

    return glob.glob(path,recursive=True)

def get_find_schema_files(schema:str, glob_path:str):

    fullpaths = find_files(glob_path)

    def find_schema(path:str):
        filename = os.path.basename(path)
        name_split = filename.split('.')
        if not len(name_split):
            return False
        
        return name_split[0] == schema

    return list(filter(find_schema, fullpaths))

def find_glob_files(glob_path:str, *, schema:str = ''):

    fullpaths = find_files(glob_path)

    if not schema:
        return fullpaths

    def find_schema(path:str):
        filename = os.path.basename(path)
        name_split = filename.split('.')
        if not len(name_split):
            return False
        
        return name_split[0] == schema

    return list(filter(find_schema, fullpaths))

def find_glob_filter(glob_path:str, *, filter_str:str = ''):
    
    fullpaths = find_files(glob_path)

    if not filter_str:
        return fullpaths

    def find_filter(path:str):
        filename = os.path.basename(path)

        return filename.startswith(filter_str)

    return list(filter(find_filter, fullpaths))

def find_identity_dataname(data_path:str):

    filename:str = os.path.basename(data_path)
    filename = os.path.splitext(filename)[0]
    filename_element = filename.split('.')
    filename_element = filename_element[1:-1]
    filename_element = '.'.join(filename_element)

    return filename_element