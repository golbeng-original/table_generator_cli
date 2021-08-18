import numpy
import re

from enum import Enum


SUPPORT_PRIMITIVE_TYPE = [
    'uint',
    'int',
    'bool',
    'float',
    'string'
]

NUMBERIC_TYPE = [
    numpy.uint32,
    numpy.int32,
    numpy.float32
]

BOOLEAN_TYPE = [
    bool
]

__numberic_regex = re.compile(r'[0-9]+.?[0-9]?')
def __is_valid_numberic(value):
    return True if __numberic_regex.match(value) else False

__bool_regex = re.compile(r'([Tt]rue|[Ff]alse)')
def __is_valid_bool(value):
    return True if __bool_regex.match(value) else False

def is_valid_primitive_value(schema_field, value:str):

    if schema_field.get_nativetype() in NUMBERIC_TYPE:
        return __is_valid_numberic(value)

    if schema_field.get_nativetype() in BOOLEAN_TYPE:
        return __is_valid_bool(value)

    return True if schema_field.get_nativetype() is str else False

def is_valid_enum_value(schema_field, enum_data, value:str):
    
    enum_meta_info =  enum_data.get_enum_meta_info(schema_field.type)
    if not enum_meta_info:
        return False

    return True if enum_meta_info.is_exist_enum_field(value) else False